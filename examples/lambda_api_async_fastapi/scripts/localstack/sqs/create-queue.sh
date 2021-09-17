if [ -z "$1" ]; then
  echo 'Queue name must be informed'
  exit 1
else
  aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name $1
fi