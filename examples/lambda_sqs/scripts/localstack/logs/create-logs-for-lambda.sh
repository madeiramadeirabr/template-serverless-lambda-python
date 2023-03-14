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

#    echo "aws --endpoint-url=http://$HOST:4566 lambda create-event-source-mapping \
#    --function-name arn:aws:lambda:$REGION:000000000000:function:$1 \
#    --event-source-arn arn:aws:sqs:$REGION:000000000000:$2"
#
#    aws --endpoint-url=http://$HOST:4566 lambda create-event-source-mapping \
#    --function-name arn:aws:lambda:$REGION:000000000000:function:$1 \
#    --event-source-arn arn:aws:sqs:$REGION:000000000000:$2

    echo 'reference: https://docs.localstack.cloud/user-guide/aws/logs/'
    echo 'reference: https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/SubscriptionFilters.html#LambdaFunctionExample'


    echo 'Creating the log group'
    echo "aws  --endpoint-url=http://$HOST:4566  logs create-log-group --log-group-name $FUNCTION_NAME --region $REGION"
    aws  --endpoint-url=http://$HOST:4566 logs create-log-group --log-group-name $FUNCTION_NAME --region $REGION

    echo 'Creating the log stream'
    echo "aws  --endpoint-url=http://$HOST:4566  logs create-log-stream --log-group-name $FUNCTION_NAME --log-stream-name $FUNCTION_NAME --region $REGION"
    aws  --endpoint-url=http://$HOST:4566 logs create-log-stream --log-group-name $FUNCTION_NAME --log-stream-name $FUNCTION_NAME --region $REGION

    echo 'Creating the permission'
    aws --endpoint-url=http://$HOST:4566 lambda add-permission \
    --function-name $FUNCTION_NAME \
    --statement-id $FUNCTION_NAME \
    --principal "logs.amazonaws.com" \
    --action "lambda:InvokeFunction" \
    --source-arn "arn:aws:logs:$REGION:000000000000:log-group:$FUNCTION_NAME" \
    --source-account "000000000000" \
    --region $REGION

    echo 'Creating the put-subscription-filter'
    aws --endpoint-url=http://$HOST:4566 logs put-subscription-filter \
        --log-group-name $FUNCTION_NAME \
        --filter-name "${FUNCTION_NAME}_logs" \
        --filter-pattern "" \
        --destination-arn arn:aws:lambda:$REGION:000000000000:function:$FUNCTION_NAME \
        --region $REGION
#        --role-arn "arn:aws:iam::000000000000:role/lambda_role"

# separar em outro script
#  echo 'Testing'
#    timestamp=$(($(date +'%s * 1000 + %-N / 1000000')))
#    aws --endpoint-url=http://$HOST:4566 logs put-log-events \
#    --log-group-name $FUNCTION_NAME \
#    --log-stream-name $FUNCTION_NAME \
#    --log-events \
#    timestamp=$timestamp,message='"{\"foo\":\"bar\", \"hello\": \"world\"}"' \
#    timestamp=$timestamp,message="my test event" \
#    timestamp=$timestamp,message='"{\"foo\":\"nomatch\"}"'
fi
