#!/bin/bash
# **************************
# Localstack Cloud Watch Put Rul
# Version: 1.0.1
# **************************
if [ -z "$1" ]; then
  echo 'Rule name must be informed'
  exit 1
else
  if [ $RUNNING_IN_CONTAINER ]; then
    HOST=localstack
  else
    HOST=0.0.0.0
  fi

  RULE=$1

  if [ -z "$2" ]; then
    TYPE="rate"
  else
    TYPE=$2
  fi

  if [ -z "$3" ]; then
    EXPRESSION="1 minute"
  else
    EXPRESSION="$3"
  fi

  if [ -z "$4" ]; then
    REGION=us-east-1
  else
    REGION=$4
  fi



  echo "https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html"
#  echo $TYPE
#  echo $EXPRESSION
#  echo $RULE
#  echo $REGION
  echo "aws --endpoint-url=http://$HOST:4566 events put-rule --schedule-expression \"$TYPE($EXPRESSION)\" --name $RULE --region $REGION"
  aws --endpoint-url=http://$HOST:4566 events put-rule --schedule-expression "$TYPE($EXPRESSION)" --name $RULE --region $REGION

fi
