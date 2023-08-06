# About

Experimental (in progress) microservice to manage the downloads of biomaj.

A protobuf interface is available in biomaj_download/message/message_pb2.py to exchange messages between BioMAJ and the download service.
Messages go through RabbitMQ (to be installed).

# Protobuf

To compile protobuf, in biomaj_download/message:

protoc --python_out=. message.proto

# Development

    flake8  biomaj_download/*.py biomaj_download/download

# Prometheus metrics

Endpoint: /api/download/metrics


# Run

## Message consumer:
export BIOMAJ_CONFIG=path_to_config.yml
python bin/biomaj_download_consumer.py

## Web server

export BIOMAJ_CONFIG=path_to_config.yml
gunicorn biomaj_download.biomaj_download_web:app

Web processes should be behind a proxy/load balancer, API base url /api/download


3.0.6:
  Fix download_or_copy to avoid downloading a file  existing in a previous production directory
3.0.4:
  Fixes on messages
3.0.3:
  Fix management of timeout leading to a crash when using biomaj.download parameter.
3.0.2:
  set rabbitmq parameter optional
3.0.1:
  add missing README etc.. in package
3.0.0:
  move download management out of biomaj main package


