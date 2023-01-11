#!/bin/bash
# **************************
# Localstack Cloud Watch List Rules Tool
# Version: 1.0.0
# **************************
if [ $RUNNING_IN_CONTAINER ]; then
  HOST=localstack
else
  HOST=0.0.0.0
fi

if [ -z $REGION_NAME ]; then
  REGION_NAME=us-east-1
fi

echo "aws --endpoint-url=http://$HOST:4566 events list-rules --region $REGION_NAME"
aws --endpoint-url=http://$HOST:4566 events list-rules --region $REGION_NAME
