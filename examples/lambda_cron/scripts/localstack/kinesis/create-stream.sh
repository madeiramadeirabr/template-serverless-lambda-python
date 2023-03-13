#!/bin/bash
if [ -z "$1" ]; then
  echo 'Stream name must be informed'
  exit 1
else
    if [ $RUNNING_IN_CONTAINER ]; then
    HOST=localstack
  else
    HOST=0.0.0.0
  fi

  QUEUE=$1

  if [ -z "$2" ]; then
    REGION=us-east-1
  else
    REGION=$2
  fi
  echo "aws --endpoint-url=http://$HOST:4566 kinesis create-stream --stream-name $1 --shard-count 2"
  aws --endpoint-url=http://$HOST:4566 kinesis create-stream \
    --stream-name $1 \
    --shard-count 2
fi
