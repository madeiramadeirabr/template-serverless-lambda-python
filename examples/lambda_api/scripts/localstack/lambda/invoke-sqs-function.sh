if [ -z "$1" ]; then
  echo 'Function name must be informed'
  exit 1
else

  HOST=0.0.0.0
  FUNCTION_PATH=$1
  FUNCTION_NAME=$1
  if test -d ./$FUNCTION_PATH; then
    PAYLOAD=./$FUNCTION_PATH/samples/localstack/SQSTest.json
  else
    PAYLOAD=./samples/localstack/SQSTest.json
  fi


  echo "Function name: $FUNCTION_NAME"
  echo "Function path: $FUNCTION_PATH"
  echo "Function ARN arn:aws:lambda:us-east-1:000000000000:$FUNCTION_NAME"

  echo "aws --endpoint-url=http://$HOST:4566 lambda invoke \
  --function-name arn:aws:lambda:us-east-1:000000000000:function:$FUNCTION_NAME \
  --payload file://$PAYLOAD ./output/response.json \
  --log-type Tail --query 'LogResult' --output text |  base64 -d"

  aws --endpoint-url=http://$HOST:4566 lambda invoke \
  --function-name arn:aws:lambda:us-east-1:000000000000:function:$FUNCTION_NAME \
  --payload file://$PAYLOAD ./output/response.json \
  --log-type Tail --query 'LogResult' --output text |  base64 -d
fi

