#!/bin/bash
if [ -z "$1" ]; then
  echo 'Queue name must be informed'
  exit 1
else
  if [ $RUNNING_IN_CONTAINER ]; then
    HOST=localstack
  else
    HOST=0.0.0.0
  fi
  echo "aws --endpoint-url=http://$HOST:4566 sqs create-queue --queue-name $1"
  aws --endpoint-url=http://$HOST:4566 sqs create-queue --queue-name $1
fi