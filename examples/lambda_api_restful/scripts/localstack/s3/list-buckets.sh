#!/bin/bash
if [ $RUNNING_IN_CONTAINER ]; then
  HOST=localstack
else
  HOST=0.0.0.0
fi
echo "aws --endpoint-url=http://$HOST:4566 s3 ls"
aws --endpoint-url=http://$HOST:4566 s3 ls