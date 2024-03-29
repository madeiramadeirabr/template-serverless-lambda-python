#!/bin/bash
# **************************
# Localstack Lambda List Functions Tool
# Version: 1.0.0
# **************************
if [ $RUNNING_IN_CONTAINER ]; then
  HOST=localstack
else
  HOST=0.0.0.0
fi

REGION=$1
if [ -z "$1" ]; then
  REGION=us-east-1
fi
#echo $REGION
aws --endpoint-url=http://$HOST:4566 lambda list-functions --region $REGION
#aws --endpoint-url=http://$HOST:4566 lambda list-functions --region $REGION
#aws --endpoint-url=http://localhost:4566 lambda list-functions --master-region us-east-1
#aws --endpoint-url=http://localhost:4566 lambda list-functions --master-region us-east-2
