if [ -z "$1" ]; then
  echo 'Queue name must be informed'
  exit 1
else
  aws --endpoint-url=http://localhost:4566 sqs get-queue-url --queue-name $1
  if [ $? -eq 0 ]; then
      aws --endpoint-url=http://localhost:4566 sqs delete-queue --queue-url http://localhost:4566/000000000000/$1
      if [ $? -eq 0 ]; then
        echo "Queue deleted"
      else
        echo "Queue not deleted"
        exit 1
      fi
  else
      echo "Queue doesn't exists"
      exit 1
  fi
fi
