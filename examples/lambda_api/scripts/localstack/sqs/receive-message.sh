QUEUE=$1
if [ -z "$QUEUE" ]
then
  QUEUE='http://localhost:4566/000000000000/test'
fi

echo "aws --endpoint-url=http://localhost:4566 sqs receive-message --queue-url $QUEUE"
aws --endpoint-url=http://localhost:4566 sqs receive-message --queue-url $QUEUE

if [ ! $? -eq 0 ]; then
    QUEUE="http://localhost:4566/000000000000/$QUEUE"
    echo "aws --endpoint-url=http://localhost:4566 sqs receive-message --queue-url $QUEUE"
    aws --endpoint-url=http://localhost:4566 sqs receive-message --queue-url $QUEUE
fi