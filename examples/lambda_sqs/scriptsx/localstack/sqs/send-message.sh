QUEUE=$1
if [ -z "$QUEUE" ]
then
  QUEUE='http://localhost:4566/000000000000/test-queue'
else
  QUEUE=$(basename -- $QUEUE)
  QUEUE="http://localhost:4566/000000000000/${QUEUE}"
fi
MESSAGE=$2
if [ -z "$MESSAGE" ]
then
  MESSAGE=$(cat samples/localstack/sqs/sample.json)
fi
#echo $QUEUE
#exit
echo "aws --endpoint-url=http://localhost:4566 sqs send-message --queue-url $QUEUE --message-body '$MESSAGE'"
aws --endpoint-url=http://localhost:4566 sqs send-message --queue-url $QUEUE --message-body "'$MESSAGE'"
