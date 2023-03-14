#!/bin/bash
# **************************
# Localstack Logs Create Logs for Lambda Tool
# Version: 1.0.0
# **************************
if [ -z "$1" ]; then
  echo 'Function name must be informed'
  exit 1
else
  if [ $RUNNING_IN_CONTAINER ]; then
    HOST=localstack
  else
    HOST=0.0.0.0
  fi

  if [ -z "$2" ]; then
  REGION=us-east-1
  else
    REGION=$2
  fi
  FUNCTION_NAME=$1

    echo 'reference: https://docs.localstack.cloud/user-guide/aws/logs/'




    #--filter-pattern "{$.foo = \"bar\"}"
    # awslocal logs filter-log-events --log-group-name test-filter --filter-pattern "{$.foo = \"bar\"}"
    aws --endpoint-url=http://$HOST:4566 logs filter-log-events \
        --log-group-name $FUNCTION_NAME \
        --filter-pattern "*" \
        --region $REGION
#        --filter-name "${FUNCTION_NAME}_logs" \
#        --destination-arn arn:aws:lambda:$REGION:000000000000:function:$FUNCTION_NAME \
#        --role-arn "arn:aws:iam::000000000000:role/lambda_role"
fi
