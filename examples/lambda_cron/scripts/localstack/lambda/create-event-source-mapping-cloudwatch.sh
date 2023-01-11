#!/bin/bash
# **************************
# Localstack Lambda Create Event Source Mapping (Cloud Watch)Tool
# Version: 1.0.0
# **************************
if [ -z "$1" ]; then
  echo 'Function name must be informed'
  exit 1
else
  if [ -z "$2" ]; then
    echo 'Rule name must be informed'
    exit 1
  else
    if [ $RUNNING_IN_CONTAINER ]; then
      HOST=localstack
    else
      HOST=0.0.0.0
    fi
    REGION=us-east-1
    echo "aws --endpoint-url=http://$HOST:4566 lambda add-permission \
    --function-name arn:aws:lambda:$REGION:000000000000:function:$1 \
    --statement-id my-scheduled-event \
    --action 'lambda:InvokeFunction' \
    --principal events.amazonaws.com \
    --source-arn arn:aws:events:$REGION:000000000000:rule/$2 \
    --region $REGION
    "

    aws --endpoint-url=http://$HOST:4566 lambda add-permission \
    --function-name arn:aws:lambda:$REGION:000000000000:function:$1 \
    --statement-id my-scheduled-event \
    --action 'lambda:InvokeFunction' \
    --principal events.amazonaws.com \
    --source-arn arn:aws:events:$REGION:000000000000:rule/$2 \
    --region $REGION

    targets=$(cat <<-END
[
  {
    "Id": "1",
    "Arn": "arn:aws:lambda:$REGION:000000000000:function:$1"
  }
]
END
)
    echo "creating the file targets.json"
    touch targets.json
    echo "putting the content"
    echo $targets > targets.json

    echo "aws --endpoint-url=http://$HOST:4566 events put-targets --rule $2 --targets file://targets.json --region $REGION"
    aws --endpoint-url=http://$HOST:4566 events put-targets --rule $2 --targets file://targets.json --region $REGION
  fi
fi
