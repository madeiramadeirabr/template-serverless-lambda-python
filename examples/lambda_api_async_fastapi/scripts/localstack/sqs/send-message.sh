QUEUE=$1
if [ -z "$QUEUE" ]
then
  QUEUE='http://localhost:4566/000000000000/test'
fi
MESSAGE=$2
if [ -z "$MESSAGE" ]
then
  #MESSAGE='test message'
  MESSAGE=$(cat tests/datasources/events/sourcing-service-decision-processor/sample.json)
fi

echo "aws --endpoint-url=http://localhost:4566 sqs send-message --queue-url $QUEUE --message-body '$MESSAGE'"
aws --endpoint-url=http://localhost:4566 sqs send-message --queue-url $QUEUE --message-body "'$MESSAGE'"
