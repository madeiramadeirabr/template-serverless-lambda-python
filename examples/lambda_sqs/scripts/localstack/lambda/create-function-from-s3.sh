if [ -z "$1" ]; then
  echo 'Function name must be informed'
  exit 1
else

  HOST=0.0.0.0
  FUNCTION_PATH=$1
  FUNCTION_NAME=$1
  HANDLER=$2
  REGION=us-east-1
  if [ -z "$2" ]; then
    HANDLER="app.index"
  fi

  if [ ! -z "$3" ]; then
    FUNCTION_PATH=$1
    FUNCTION_NAME=$2
    HANDLER=$3
  fi

  echo "Function name: $FUNCTION_NAME"
  echo "Function path: $FUNCTION_PATH"
  echo "Function handler: $HANDLER"


  # zip full code
  if test -f lambda-full.zip; then
    rm lambda-full.zip
  fi

  #check path
  if test -d ./$FUNCTION_PATH; then
    echo "Changing dir ./$(FUNCTION_PATH)"
    cd ./$FUNCTION_PATH
    echo "Zipping data from $(pwd)"
    # python3 ../scripts/tools/python/zip.py --zip_file=../lambda-full.zip --source_dir=.
    zip -r ../lambda-full.zip ./ -x '*.git*' -x './zip.sh*' -x './venv/*' -x './.idea/*'
  else
    echo "Zipping data from $(pwd)"
    # python3 ./scripts/tools/python/zip.py --zip_file=./lambda-full.zip --source_dir=.
    zip -r ./lambda-full.zip ./ -x '*.git*' -x './zip.sh*' -x './venv/*' -x './.idea/*'
  fi

  if test -d ./$FUNCTION_PATH; then
    echo "Changing dir ../"
    cd ../
  fi

  echo 'Try to list'
  echo "aws --endpoint-url=http://$HOST:4566 s3api list-objects --bucket test > /dev/null 2>&1"
  aws --endpoint-url=http://$HOST:4566 s3api list-objects --bucket test > /dev/null 2>&1

  if [ $? -ne 0 ]; then
    echo 'Create the bucket'
    echo "aws --endpoint-url=http://$HOST:4566 s3 mb s3://test"
    aws --endpoint-url=http://$HOST:4566 s3 mb s3://test
  fi

  echo 'Copy lambda zip file to S3'
  echo "aws --endpoint-url=http://$HOST:4566 s3 cp lambda-full.zip s3://test"
  aws --endpoint-url=http://$HOST:4566 s3 cp lambda-full.zip s3://test

  echo 'Check if the lambda function exits'
  echo "aws --endpoint-url=http://$HOST:4566 lambda get-function --function-name $FUNCTION_NAME --region $REGION > /dev/null 2>&1"
  aws --endpoint-url=http://$HOST:4566 lambda get-function --function-name $FUNCTION_NAME --region $REGION > /dev/null 2>&1

  if [ $? -eq 0 ]; then
    echo 'Delete the last lambda'
    echo "aws --endpoint-url=http://$HOST:4566 lambda delete-function --function-name $FUNCTION_NAME --region $REGION"
    aws --endpoint-url=http://$HOST:4566 lambda delete-function --function-name $FUNCTION_NAME --region $REGION
  fi

  echo "Creating the environment variables"
  if test -d ./$FUNCTION_PATH; then
    if test -d ./$FUNCTION_PATH/.chalice; then
      ENVIRONMENT_VARIABLES=$(jq '.stages.dev.environment_variables' ./$FUNCTION_PATH/.chalice/config.json -c)
    else
      #ENVIRONMENT_VARIABLES=$(python3 ../scripts/tools/python/env-to-json.py ./$FUNCTION_PATH/env/development.env | jq)
      ENVIRONMENT_VARIABLES=$(python3 ../scripts/tools/python/env-to-json.py ./env/development.env)
      #jq $(python3 ../scripts/tools/python/env-to-json.py ./env/development.env) -c
    fi
  else
    if test -d ./$FUNCTION_PATH/.chalice; then
      ENVIRONMENT_VARIABLES=$(jq '.stages.dev.environment_variables' ./.chalice/config.json -c)
    else
      #ENVIRONMENT_VARIABLES=$(python3 ./scripts/tools/python/env-to-json.py ./env/development.env | jq)
      ENVIRONMENT_VARIABLES=$(python3 ./scripts/tools/python/env-to-json.py ./env/development.env)
      #jq $(python3 ./scripts/tools/python/env-to-json.py ./env/development.env) -c
    fi
  fi
#  echo 'exit'
#  echo $ENVIRONMENT_VARIABLES

#  echo "{\"Variables\": $ENVIRONMENT_VARIABLES }"
#  echo {"Variables": $ENVIRONMENT_VARIABLES} > environment.json

  echo "Creating the lambda function"
  echo "aws --endpoint-url=http://$HOST:4566 lambda create-function \
   --function-name arn:aws:lambda:$REGION:000000000000:function:$FUNCTION_NAME \
   --runtime python3.6 --handler $HANDLER --memory-size 128 \
   --code S3Bucket=test,S3Key=lambda-full.zip --role arn:aws:iam:awslocal \
   --environment {\"Variables\": $ENVIRONMENT_VARIABLES}"

  aws --endpoint-url=http://$HOST:4566 lambda create-function \
   --function-name arn:aws:lambda:$REGION:000000000000:function:$FUNCTION_NAME \
   --runtime python3.6 --handler $HANDLER --memory-size 128 \
   --code S3Bucket=test,S3Key=lambda-full.zip --role arn:aws:iam:awslocal \
   --environment "{\"Variables\": $ENVIRONMENT_VARIABLES }"
   #--environment Variables="{ENVIRONMENT_NAME=development}"
   # --environment file://environment.json
fi
