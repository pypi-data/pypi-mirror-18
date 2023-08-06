import ssl
import os
import pkg_resources
import shutil
import yaml
import configparser
import logging
import json
import datetime
import time

from flask import Flask
from flask import jsonify
from flask import request
from flask import abort

import requests

from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client.exposition import generate_latest

import consul
import redis
from pymongo import MongoClient
import pika

from tabulate import tabulate

from biomaj.bank import Bank
from biomaj.schema_version import SchemaVersion

from biomaj.options import Options as BmajOptions
from biomaj_core.config import BiomajConfig
from biomaj_core.utils import Utils
from biomaj.workflow import Workflow
from biomaj.workflow import UpdateWorkflow
from biomaj.workflow import RemoveWorkflow

config_file = 'config.yml'
if 'BIOMAJ_CONFIG' in os.environ:
        config_file = os.environ['BIOMAJ_CONFIG']

config = None
with open(config_file, 'r') as ymlfile:
    config = yaml.load(ymlfile)
    Utils.service_config_override(config)

BiomajConfig.load_config(config['biomaj']['config'])

last_status_check = None
last_status = None

data_dir = BiomajConfig.global_config.get('GENERAL', 'data.dir')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
log_dir = BiomajConfig.global_config.get('GENERAL', 'log.dir')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
process_dir = BiomajConfig.global_config.get('GENERAL', 'process.dir')
if not os.path.exists(process_dir):
    os.makedirs(process_dir)
cache_dir = BiomajConfig.global_config.get('GENERAL', 'cache.dir')
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)
lock_dir = BiomajConfig.global_config.get('GENERAL', 'lock.dir')
if not os.path.exists(lock_dir):
    os.makedirs(lock_dir)

redis_client = redis.StrictRedis(
    host=config['redis']['host'],
    port=config['redis']['port'],
    db=config['redis']['db'],
    decode_responses=True
)

logging.info("Check database schema and upgrade if necessary")
SchemaVersion.migrate_pendings()

app = Flask(__name__)

biomaj_metric = Counter("biomaj_daemon_total", "Bank total update execution.", ['bank'])
biomaj_error_metric = Counter("biomaj_daemon_errors", "Bank total update errors.", ['bank'])
biomaj_time_metric = Gauge("biomaj_daemon_time", "Bank update execution time in seconds.", ['bank'])


def consul_declare(config):
    if config['consul']['host']:
        consul_agent = consul.Consul(host=config['consul']['host'])
        consul_agent.agent.service.register('biomaj-daemon', service_id=config['consul']['id'], address=config['web']['hostname'], port=config['web']['port'], tags=['biomaj'])
        check = consul.Check.http(url='http://' + config['web']['hostname'] + ':' + str(config['web']['port']) + '/api/daemon', interval=20)
        consul_agent.agent.check.register(config['consul']['id'] + '_check', check=check, service_id=config['consul']['id'])


consul_declare(config)

OPTIONS_PARAMS = {
    'config': None,
    'check': False,
    'update': False,
    'fromscratch': False,
    'publish': False,
    'unpublish': False,
    'release': None,
    'from_task': None,
    'process': None,
    'log': None,
    'remove': False,
    'removeall': False,
    'removepending': False,
    'status': False,
    'bank': None,
    'owner': None,
    'stop_before': None,
    'stop_after': None,
    'freeze': False,
    'unfreeze': False,
    'force': False,
    'help': False,
    'search': False,
    'formats': None,
    'types': None,
    'query': None,
    'show': False,
    'newbank': None,
    'newdir': None,
    'visibility': None,
    'maintenance': None,
    'version': False,
    'statusko': False,
    'trace': False
}


class Options(object):
    def __init__(self, d):
        self.__dict__ = d
        for key in list(OPTIONS_PARAMS.keys()):
            if not self.has_option(key):
                setattr(self, key, OPTIONS_PARAMS[key])

    def has_option(self, option):
        if hasattr(self, option):
            return True
        else:
            return False

    def get_option(self, option):
        """
        Gets an option if present, else return None
        """
        if hasattr(self, option):
            return getattr(self, option)
        return None


@app.route('/api/daemon', methods=['GET'])
def ping():
    return jsonify({'msg': 'pong'})


def biomaj_version(options):
    '''
    Get biomaj version
    '''
    version = pkg_resources.require('biomaj')[0].version
    return (True, 'Version: ' + str(version))


def check_options(options):
    if options.stop_after or options.stop_before or options.from_task:
        available_steps = []
        for flow in UpdateWorkflow.FLOW:
            available_steps.append(flow['name'])
        for flow in RemoveWorkflow.FLOW:
            available_steps.append(flow['name'])
        if options.stop_after:
            if options.stop_after not in available_steps:
                return (False, 'Invalid step: ' + options.stop_after)
        if options.stop_before:
            if options.stop_before not in available_steps:
                return (False, 'Invalid step: ' + options.stop_before)
        if options.from_task:
            if options.from_task not in available_steps:
                return (False, 'Invalid step: ' + options.from_task)
    return (True, None)


def biomaj_maintenance(options):
    '''
    Maintenance management
    '''
    if options.maintenance not in ['on', 'off', 'status']:
        print("Wrong maintenance value [on,off,status]")
        return (False, "Wrong maintenance value [on,off,status]")

    data_dir = BiomajConfig.global_config.get('GENERAL', 'data.dir')
    if BiomajConfig.global_config.has_option('GENERAL', 'lock.dir'):
        lock_dir = BiomajConfig.global_config.get('GENERAL', 'lock.dir')
    else:
        lock_dir = data_dir

    maintenance_lock_file = os.path.join(lock_dir, 'biomaj.lock')
    if options.maintenance == 'status':
        if os.path.exists(maintenance_lock_file):
            return (True, "Maintenance: On")
        else:
            return (True, "Maintenance: Off")

    if options.maintenance == 'on':
        f = open(maintenance_lock_file, 'w')
        f.write('1')
        f.close()
        return (True, "Maintenance set to On")

    if options.maintenance == 'off':
        if os.path.exists(maintenance_lock_file):
            os.remove(maintenance_lock_file)
        return (True, "Maintenance set to Off")


def biomaj_owner(options):
    '''
    Bank ownership management
    '''
    if not options.bank:
        return (False, "Bank option is missing")
    bank = Bank(options.bank, options=options, no_log=True)
    bank.set_owner(options.owner)
    return (True, None)


def biomaj_visibility(options):
    '''
    Bank visibility management
    '''
    if not options.bank:
        return (False, "Bank option is missing")
    if options.visibility not in ['public', 'private']:
        return (False, "Valid values are public|private")

    bank = Bank(options.bank, options=options, no_log=True)
    bank.set_visibility(options.visibility)
    return (True, "Do not forget to update accordingly the visibility.default parameter in the configuration file")


def biomaj_move_production_directories(options):
    '''
    Change bank production directories
    '''
    if not options.bank:
        return (False, "Bank option is missing")

    if not os.path.exists(options.newdir):
        return (False, "Destination directory does not exists")

    bank = Bank(options.bank, options=options, no_log=True)
    if not bank.bank['production']:
        return (False, "Nothing to move, no production directory")

    bank.load_session(Workflow.FLOW, None)
    w = Workflow(bank)
    res = w.wf_init()
    if not res:
        return (False, 'Bank initialization failure')

    for prod in bank.bank['production']:
        session = bank.get_session_from_release(prod['release'])
        bank.load_session(Workflow.FLOW, session)
        prod_path = bank.session.get_full_release_directory()
        if os.path.exists(prod_path):
            shutil.move(prod_path, options.newdir)
        prod['data_dir'] = options.newdir
    bank.banks.update({'name': options.bank}, {'$set': {'production': bank.bank['production']}})
    w.wf_over()
    return (True, "Bank production directories moved to " + options.newdir + "\nWARNING: do not forget to update accordingly the data.dir and dir.version properties")


def biomaj_newbank(options):
    '''
    Rename a bank
    '''
    if not options.bank:
        return (False, "Bank option is missing")

    bank = Bank(options.bank, options=options, no_log=True)
    conf_dir = BiomajConfig.global_config.get('GENERAL', 'conf.dir')
    bank_prop_file = os.path.join(conf_dir, options.bank + '.properties')
    config_bank = configparser.SafeConfigParser()
    config_bank.read([os.path.join(conf_dir, options.bank + '.properties')])
    config_bank.set('GENERAL', 'db.name', options.newbank)
    newbank_prop_file = open(os.path.join(conf_dir, options.newbank + '.properties'), 'w')
    config_bank.write(newbank_prop_file)
    newbank_prop_file.close()
    bank.banks.update({'name': options.bank}, {'$set': {'name': options.newbank}})
    os.remove(bank_prop_file)
    return (True, "Bank " + options.bank + " renamed to " + options.newbank)


def biomaj_search(options):
    '''
    Search within banks
    '''
    msg = ''
    if options.query:
        res = Bank.searchindex(options.query)
        msg += 'Query matches for :' + options.query + '\n'
        results = [["Release", "Format(s)", "Type(s)", "Files"]]
        for match in res:
            results.append([match['_source']['release'],
                            str(match['_source']['format']),
                            str(match['_source']['types']),
                            ','.join(match['_source']['files'])])
        msg += tabulate(results, headers="firstrow", tablefmt="grid")
    else:
        formats = []
        if options.formats:
            formats = options.formats.split(',')
        types = []
        if options.types:
            types = options.types.split(',')
        msg += "Search by formats=" + str(formats) + ", types=" + str(types) + '\n'
        res = Bank.search(formats, types, False)
        results = [["Name", "Release", "Format(s)", "Type(s)", 'Published']]
        for bank in sorted(res, key=lambda bank: (bank['name'])):
            b = bank['name']
            bank['production'].sort(key=lambda n: n['release'], reverse=True)
            for prod in bank['production']:
                iscurrent = ""
                if prod['session'] == bank['current']:
                    iscurrent = "yes"
                results.append([b if b else '', prod['release'], ','.join(prod['formats']),
                                ','.join(prod['types']), iscurrent])
        msg += tabulate(results, headers="firstrow", tablefmt="grid")
    return (True, msg)


def biomaj_show(options):
    '''
    show bank details
    '''
    if not options.bank:
        return (False, "Bank option is required")

    bank = Bank(options.bank, options=options, no_log=True)
    results = [["Name", "Release", "Format(s)", "Type(s)", "Tag(s)", "File(s)"]]
    current = None
    fformat = None
    if 'current' in bank.bank and bank.bank['current']:
        current = bank.bank['current']
    for prod in bank.bank['production']:
        include = True
        release = prod['release']
        if current == prod['session']:
            release += ' (current)'
        if options.release and (prod['release'] != options.release and prod['prod_dir'] != options.release):
            include = False
        if include:
            session = bank.get_session_from_release(prod['release'])
            formats = session['formats']
            afiles = []
            atags = []
            atypes = []
            for fformat in list(formats.keys()):
                for elt in formats[fformat]:
                    atypes.append(','.join(elt['types']))
                    for tag in list(elt['tags'].keys()):
                        atags.append(elt['tags'][tag])
                    for eltfile in elt['files']:
                        afiles.append(eltfile)
            results.append([
                bank.bank['name'],
                release,
                fformat,
                ','.join(atypes),
                ','.join(atags),
                ','.join(afiles)])
    msg = tabulate(results, headers="firstrow", tablefmt="grid")
    return (True, msg)


def biomaj_check(options):
    '''
    Check bank properties
    '''
    if not options.bank:
        return (False, "Bank name is missing")

    bank = Bank(options.bank, options=options, no_log=True)
    msg = options.bank + " check: " + str(bank.check()) + "\n"
    return (True, msg)


def biomaj_status(options):
    '''
    Get bank status information
    '''
    msg = ''
    if options.bank:
        bank = Bank(options.bank, options=options, no_log=True)
        if bank.bank['properties']['visibility'] != 'public' and not bank.is_owner():
            return (False, 'Access forbidden')
        info = bank.get_bank_release_info(full=True)
        msg += tabulate(info['info'], headers='firstrow', tablefmt='psql') + '\n'
        msg += tabulate(info['prod'], headers='firstrow', tablefmt='psql') + '\n'
        # do we have some pending release(s)
        if 'pend' in info and len(info['pend']) > 1:
            msg += tabulate(info['pend'], headers='firstrow', tablefmt='psql') + '\n'
    else:
        banks = Bank.list()
        # Headers of output table
        banks_list = [["Name", "Type(s)", "Release", "Visibility", "Last update"]]
        for bank in sorted(banks, key=lambda k: k['name']):
            bank = Bank(bank['name'], options=options, no_log=True)
            if bank.bank['properties']['visibility'] == 'public' or bank.is_owner():
                banks_list.append(bank.get_bank_release_info()['info'])
        msg += tabulate(banks_list, headers="firstrow", tablefmt="psql") + '\n'
    return (True, msg)


def biomaj_status_ko(options):
    '''
    Get failed banks
    '''
    banks = Bank.list()
    banks_list = [["Name", "Type(s)", "Release", "Visibility", "Last run"]]
    for bank in sorted(banks, key=lambda k: k['name']):
        try:
            bank = Bank(bank['name'], options=options, no_log=True)
            bank.load_session(UpdateWorkflow.FLOW)
            if bank.session is not None:
                if bank.use_last_session and not bank.session.get_status(Workflow.FLOW_OVER):
                    wf_status = bank.session.get('workflow_status')
                    if wf_status is None or not wf_status:
                        banks_list.append(bank.get_bank_release_info()['info'])
        except Exception as e:
            return (False, str(e))
    return (True, tabulate(banks_list, headers="firstrow", tablefmt="psql"))


def biomaj_bank_update_request(options):
    '''
    Send bank update request to rabbitmq
    '''
    return biomaj_send_message(options)


def biomaj_send_message(options):
    '''
    Send message to rabbitmq listener
    '''
    cur = datetime.datetime.now()
    options.timestamp = time.mktime(cur.timetuple())
    redis_client.lpush(config['redis']['prefix'] + ':queue', json.dumps(options.__dict__))
    return (True, None)


def biomaj_bank_update(options):
    '''
    Update a bank
    '''
    if not options.bank:
        return (False, "Bank name is missing")
    banks = options.bank.split(',')
    gres = True
    msg = ''
    for bank in banks:
        options.bank = bank
        bmaj = Bank(bank, options=options, no_log=True)
        if bmaj.is_locked():
            return (False, 'Bank is locked due to an other action')
        check_status = bmaj.check()
        if not check_status:
            msg += 'Skip bank ' + options.bank + ': wrong config\n'
            gres = False
            continue
        else:
            msg += 'Bank update request sent for ' + options.bank + '\n'
            if not options.proxy:
                res = bmaj.update(depends=True)
                return (res, '')
            res = biomaj_bank_update_request(options)
            if not res:
                msg += 'Failed to send update request for ' + options.bank + '\n'

    if not gres:
        return (False, msg)
    return (True, msg)


def biomaj_freeze(options):
    '''
    freeze a bank
    '''
    if not options.bank:
        return (False, "Bank name is missing")
    if not options.release:
        return (False, "Bank release is missing")
    bmaj = Bank(options.bank, options=options)
    res = bmaj.freeze(options.release)
    if not res:
        return (False, 'Failed to freeze the bank release')
    return (True, None)


def biomaj_unfreeze(options):
    '''
    unfreeze a bank
    '''
    if not options.bank:
        return (False, "Bank name is missing")
    if not options.release:
        return (False, "Bank release is missing")

    bmaj = Bank(options.bank, options=options)
    res = bmaj.unfreeze(options.release)
    if not res:
        return (False, 'Failed to unfreeze the bank release')
    return (True, None)


def biomaj_remove_request(options):
    '''
    Send remove request to rabbitmq
    '''
    return biomaj_send_message(options)


def biomaj_remove(options):
    '''
    Remove a bank
    '''
    if not options.bank:
        return (False, "Bank name is missing")

    if options.remove and not options.release:
        return (False, "Bank release is missing")

    bmaj = Bank(options.bank, options=options, no_log=True)
    if bmaj.is_locked():
        return (False, 'Bank is locked due to an other action')

    res = True
    if options.removeall:
        if not options.proxy:
            res = bmaj.removeAll(options.force)
            return (res, '')
        res = biomaj_remove_request(options)
    else:
        if not options.proxy:
            res = bmaj.remove(options.release)
            return (res, '')
        res = biomaj_remove_request(options)
    if not res:
        return (False, 'Failed to send removal request')
    return (True, 'Bank removal request sent')


def biomaj_remove_pending_request(options):
    '''
    Send remove pending request to rabbitmq
    '''
    return biomaj_send_message(options)


def biomaj_remove_pending(options):
    '''
    Remove pending releases
    '''
    if not options.bank:
        return (False, "Bank name is missing")
    bmaj = Bank(options.bank, options=options, no_log=True)
    if bmaj.is_locked():
        return (False, 'Bank is locked due to an other action')
    if not options.proxy:
        res = bmaj.remove_pending(options.release)
        return (res, '')
    res = biomaj_remove_pending_request(options)
    if not res:
        return (False, 'Failed to send removal request')
    return (True, 'Request sent')


def biomaj_unpublish(options):
    '''
    Unpublish a bank
    '''
    if not options.bank:
        return (False, "Bank name is missing")

    bmaj = Bank(options.bank, options=options, no_log=True)
    bmaj.load_session()
    bmaj.unpublish()
    return (True, None)


def biomaj_publish(options):
    '''
    Publish a bank
    '''
    if not options.bank:
        return (False, "Bank name or release is missing")
    bmaj = Bank(options.bank, options=options, no_log=True)
    bmaj.load_session()
    bank = bmaj.bank
    session = None
    if options.get_option('release') is None:
        # Get latest prod release
        if len(bank['production']) > 0:
            prod = bank['production'][len(bank['production']) - 1]
            for s in bank['sessions']:
                if s['id'] == prod['session']:
                    session = s
                    break
    else:
        # Search production release matching release
        for prod in bank['production']:
            if prod['release'] == options.release or prod['prod_dir'] == options.release:
                # Search session related to this production release
                for s in bank['sessions']:
                    if s['id'] == prod['session']:
                        session = s
                        break
                break
    if session is None:
        return (False, "No production session could be found for this release")
    bmaj.session._session = session
    bmaj.publish()
    return (True, None)


def biomaj_update_cancel(options):
    '''
    Cancel current update of a Bank

    Running actions (download, process) will continue on remote services but will not manage next actions.
    Biomaj process will exit when ready with a *False* status.
    '''
    if not options.bank:
        return (False, "Bank name is missing")
    redis_client.set(config['redis']['prefix'] + ':' + options.bank + ':action:cancel', 1)
    return (True, 'Requested to cancel update of bank ' + options.bank + ', update will stop once current actions are over')


def biomaj_update_status(options):
    '''
    get the status of a bank during an update cycle
    '''
    pending = redis_client.llen(config['redis']['prefix'] + ':queue')
    pending_actions = [['Pending actions', 'Date']]
    for index in range(pending):
        pending_action = redis_client.lindex(config['redis']['prefix'] + ':queue', index)
        if pending_action:
            pending_bank = json.loads(pending_action)
            action_time = datetime.datetime.utcfromtimestamp(pending_bank['timestamp'])
            if pending_bank['bank'] == options.bank:
                if pending_bank['update']:
                    pending_actions.append(['Update', action_time])
                elif pending_bank['remove'] or pending_bank['removeall']:
                    pending_actions.append(['Removal - release ' + str(pending_bank['release']), action_time])

    bmaj = Bank(options.bank, options=options, no_log=True)
    if 'status' not in bmaj.bank:
        return (True, 'No update information available')
    status_info = bmaj.bank['status']

    msg = [["Workflow step", "Status"]]

    if 'log_file' in status_info:
        msg.append(['log_file', str(status_info['log_file']['status'])])
    if 'session' in status_info:
        msg.append(['session', str(status_info['session'])])
    for flow in UpdateWorkflow.FLOW:
        step = flow['name']
        if step in status_info:
            if status_info[step]['status'] is True:
                msg.append([step, 'over'])
            elif status_info[step]['status'] is False:
                msg.append([step, 'error'])
            else:
                if status_info[Workflow.FLOW_OVER]['status'] is True:
                    msg.append([step, 'skipped'])
                else:
                    msg.append([step, 'waiting'])
        if step in ['postprocess', 'preprocess', 'removeprocess']:
            progress = status_info[step]['progress']
            for proc in list(progress.keys()):
                msg.append([proc, str(progress[proc])])
    return (True, tabulate(pending_actions, headers="firstrow", tablefmt="grid") + tabulate(msg, headers="firstrow", tablefmt="grid"))


def biomaj_user_info(options):
    '''
    Get user info, need login/password
    '''
    if not options.userlogin or not options.userpassword:
        return (False, 'Missing login or password')
    if not options.proxy:
        return (False, 'Missing proxy information')
    bindinfo = {'type': 'password', 'value': options.userpassword}
    try:
        r = requests.post(config['web']['local_endpoint'] + '/api/user/bind/user/' + options.user, json=bindinfo)
        if not r.status_code == 200:
            abort(401, {'message': 'Invalid credentials'})
        user = r.json()['user']
    except Exception as e:
        return (False, 'Connection error to proxy: ' + str(e))
    msg = 'User: ' + str(user['id']) + '\n'
    msg += 'Email: ' + str(user['email']) + '\n'
    msg += 'Api key: ' + str(user['apikey']) + '\n'
    return (True, msg)


def biomaj_client_action(options):
    check_options(options)
    if options.version:
        return biomaj_version(options)

    if options.maintenance:
        return biomaj_maintenance(options)

    if options.owner:
        return biomaj_owner(options)

    if options.visibility:
        return biomaj_visibility(options)

    if options.newdir:
        return biomaj_move_production_directories(options)

    if options.newbank:
        return biomaj_newbank(options)

    if options.search:
        return biomaj_search(options)

    if options.show:
        return biomaj_show(options)

    if options.check:
        return biomaj_check(options)

    if options.status:
        return biomaj_status(options)

    if options.statusko:
        return biomaj_status_ko(options)

    if options.update:
        return biomaj_bank_update(options)

    if options.freeze:
        return biomaj_freeze(options)

    if options.unfreeze:
        return biomaj_unfreeze(options)

    if options.remove or options.removeall:
        return biomaj_remove(options)

    if options.removepending:
        return biomaj_remove_pending(options)

    if options.unpublish:
        return biomaj_unpublish(options)

    if options.publish:
        return biomaj_publish(options)

    if options.updatestatus:
        return biomaj_update_status(options)

    if options.updatecancel:
        return biomaj_update_cancel(options)

    if options.aboutme:
        return biomaj_user_info(options)


@app.route('/api/daemon/status', methods=['GET'])
def biomaj_status_info():
    '''
    if last_status_check is not None:
        cur = datetime.datetime.now()
        if (cur - last_status_check).total_seconds() < 10:
            return status
    last_status_check = datetime.datetime.now()
    '''
    status = {
        'status': [{'service': 'biomaj-public-proxy', 'status': 1, 'count': 1}],
        'biomaj_services': [],
        'general_services': [{
            'id': 'biomaj-public-proxy',
            'host': '',
            'status': True
        }]
    }

    # Check redis
    logging.debug("Status: check redis")
    redis_ok = False
    try:
        pong = redis_client.ping()
        if pong:
            redis_ok = True
    except Exception as e:
        logging.error('Failed to ping redis: ' + str(e))
    if not redis_ok:
        status['status'].append({'service': 'biomaj-redis', 'status': -1, 'count': 0})
    else:
        status['status'].append({'service': 'biomaj-redis', 'status': 1, 'count': 1})
        status['general_services'].append({
                    'id': 'biomaj-redis',
                    'host': config['redis']['host'],
                    'status': True
        })

    # Check internal proxy
    r = requests.get(config['web']['local_endpoint'] + '/api/user')
    if not r.status_code == 200:
        status['status'].append({'service': 'biomaj-internal-proxy', 'status': -1, 'count': 0})
    else:
        status['status'].append({'service': 'biomaj-internal-proxy', 'status': 1, 'count': 1})
        status['general_services'].append({
                    'id': 'biomaj-internal-proxy',
                    'host': config['web']['local_endpoint'],
                    'status': True
        })

    # Check mongo
    logging.debug("Status: check mongo")
    if 'mongo' in config:
        mongo_ok = False
        try:
            biomaj_mongo = MongoClient(config['mongo']['url'])
            biomaj_mongo.server_info()
            mongo_ok = True
        except Exception as e:
            logging.error('Failed to connect to mongo')
        if not mongo_ok:
            status['status'].append({'service': 'biomaj-mongo', 'status': -1, 'count': 0})
        else:
            status['status'].append({'service': 'biomaj-mongo', 'status': 1, 'count': 1})
            status['general_services'].append({
                        'id': 'biomaj-mongo',
                        'host': config['mongo']['url'],
                        'status': True
            })

    # Check rabbitmq
    logging.debug("Status: check rabbit")
    if 'rabbitmq' in config and 'host' in config['rabbitmq'] and config['rabbitmq']['host']:
        rabbit_ok = False
        channel = None
        try:
            connection = None
            rabbitmq_port = config['rabbitmq']['port']
            rabbitmq_user = config['rabbitmq']['user']
            rabbitmq_password = config['rabbitmq']['password']
            rabbitmq_vhost = config['rabbitmq']['virtual_host']
            if rabbitmq_user:
                credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
                connection = pika.BlockingConnection(pika.ConnectionParameters(config['rabbitmq']['host'], rabbitmq_port, rabbitmq_vhost, credentials))
            else:
                connection = pika.BlockingConnection(pika.ConnectionParameters(config['rabbitmq']['host']))
            channel = connection.channel()
            rabbit_ok = True
        except Exception as e:
            logging.error('Rabbitmq connection error: ' + str(e))
        finally:
            if channel:
                channel.close()
        if not rabbit_ok:
            status['status'].append({'service': 'biomaj-rabbitmq', 'status': -1, 'count': 0})
        else:
            status['status'].append({'service': 'biomaj-rabbitmq', 'status': 1, 'count': 1})
            status['general_services'].append({
                        'id': 'biomaj-rabbitmq',
                        'host': config['rabbitmq']['host'],
                        'status': True
            })

    logging.debug("Status: check consul services")
    r = requests.get('http://' + config['consul']['host'] + ':8500/v1/agent/services')
    if not r.status_code == 200:
        status['status'].append({'service': 'biomaj-consul', 'status': -1, 'count': 0})
        last_status = status
        return status

    status['status'].append({'service': 'biomaj-consul', 'status': 1, 'count': 1})
    status['general_services'].append({
                'id': 'biomaj-consul',
                'host': config['consul']['host'],
                'status': True
    })

    consul_services = r.json()
    services = []
    for consul_service in list(consul_services.keys()):
        current_service = consul_services[consul_service]['Service']
        if current_service in services or current_service == 'consul':
            continue
        else:
            services.append(current_service)
        check_r = requests.get('http://' + config['consul']['host'] + ':8500/v1/health/service/' + consul_services[consul_service]['Service'])
        if not check_r.status_code == 200:
            status['status'].append({'service': 'biomaj-consul', 'status': -1, 'count': 0})
            last_status = status
            return status
        checks = check_r.json()
        nb_service = 0
        nb_service_ok = 0
        for service_check in checks:
            nb_service += 1
            check_status = True
            for check in service_check['Checks']:
                if check['Status'] != 'passing':
                    check_status = False
                    break
            if check_status:
                nb_service_ok += 1
            status['biomaj_services'].append({
                'id': service_check['Service']['Service'],
                'host': service_check['Service']['Address'],
                'status': check_status
            })
        check_status = -1
        if nb_service == nb_service_ok:
            check_status = 1
        else:
            check_status = 0
        status['status'].append({'service': consul_services[consul_service]['Service'], 'count': nb_service, 'status': check_status})

    # Check missing services
    biomaj_services = ['biomaj-watcher', 'biomaj-daemon', 'biomaj-download', 'biomaj-process', 'biomaj-user']
    for biomaj_service in biomaj_services:
        if biomaj_service not in services:
            status['status'].append({'service': biomaj_service, 'count': 0, 'status': -1})

    last_status = status

    return jsonify(status)


@app.route('/api/daemon', methods=['POST'])
def biomaj_daemon():
    '''
    List users
    '''
    apikey = request.headers.get('Authorization')
    token = None

    if apikey:
        bearer = apikey.split()
        if bearer[0] == 'APIKEY':
            token = bearer[1]
    try:
        params = request.get_json()
        options = params['options']
        options_object = Options(options)
        options_object.token = token
        options_object.user = None
        options_object.redis_host = config['redis']['host']
        options_object.redis_port = config['redis']['port']
        options_object.redis_db = config['redis']['db']
        options_object.redis_prefix = config['redis']['prefix']

        user = None
        if token:
            r = requests.get(config['web']['local_endpoint'] + '/api/user/info/apikey/' + token)
            if not r.status_code == 200:
                abort(404, {'message': 'Invalid API Key or connection issue'})
            user = r.json()['user']
            if user:
                options_object.user = user['id']

        if options_object.bank:
            bmaj_options = BmajOptions(options_object)
            BiomajConfig(options_object.bank, bmaj_options)

            if not options_object.search and not options_object.show and not options_object.check and not options_object.status:
                if not user:
                    abort(403, {'message': 'This action requires authentication with api key'})

        (res, msg) = biomaj_client_action(options_object)
    except Exception as e:
        logging.exception(e)
        return jsonify({'status': False, 'msg': str(e)})
    return jsonify({'status': res, 'msg': msg})


@app.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest()


@app.route('/api/daemon/metrics', methods=['POST'])
def add_metrics():
    '''
    Expects a JSON request with an array of {'bank': 'bank_name', 'error': 'error_message', 'execution_time': seconds_to_execute}
    '''
    procs = request.get_json()
    for proc in procs:
        if 'error' in proc and proc['error']:
            biomaj_error_metric.labels(proc['bank']).inc()
        else:
            biomaj_metric.labels(proc['bank']).inc()
            biomaj_time_metric.labels(proc['bank']).set(proc['execution_time'])
    return jsonify({'msg': 'OK'})

if __name__ == "__main__":
    context = None
    if config['tls']['cert']:
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(config['tls']['cert'], config['tls']['key'])
    app.run(host='0.0.0.0', port=config['web']['port'], ssl_context=context, threaded=True, debug=config['web']['debug'])
