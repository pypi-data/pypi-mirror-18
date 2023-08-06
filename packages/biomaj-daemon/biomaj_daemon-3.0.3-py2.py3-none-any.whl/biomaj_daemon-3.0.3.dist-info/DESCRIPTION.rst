# About

Experimental (in progress) microservice to manage biomaj.

Needs mongo and redis



# Development

    flake8 --ignore E501 biomaj_daemon

# Prometheus metrics

Endpoint: /api/download/metrics


# Run

## Message consumer:
export BIOMAJ_CONFIG=path_to_config.yml
python bin/biomaj_daemon_consumer.py

## Web server

In bin directory:
export BIOMAJ_CONFIG=path_to_config.yml
gunicorn biomaj_daemon.daemon.biomaj_daemon_web:app

Web processes should be behind a proxy/load balancer, API base url /api/daemon


3.0.3:
  Fix missing parameters
3.0.2:
  Move options to management to utils for reuse
  Fix --about-me
3.0.1:
  Micro service to manage biomaj updates


