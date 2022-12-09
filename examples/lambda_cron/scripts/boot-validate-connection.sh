#!/bin/bash
if [ $RUNNING_IN_CONTAINER ]; then
  HOST=localstack
else
  HOST=0.0.0.0
fi
do_request () {
  response=$(curl --write-out '%{http_code}' --silent --output /dev/null http://$HOST:4566)
#  echo "response: $response"
  if [ $response -eq "000" ]; then
    # error
    return 1
  elif [ $response -ne "500" ]; then
    # success
    return 0
  else
    # error
    return 1
  fi

}
#echo 'wait for the localstack boot (20 secs)'
#sleep 20

attempt_counter=0
max_attempts=40

while [ true ]
do
    # curl --write-out '%{http_code}' --silent --output /dev/null http://0.0.0.0:4566
    body=$(curl http://$HOST:4566)
    echo $body

    do_request
    if [ $? -eq 0 ]; then
      echo 'Connected'
      break
#      exit 0
    fi

    if [ ${attempt_counter} -eq ${max_attempts} ];then
      echo "Max attempts reached"
      exit 1
    fi

    printf '.'

    attempt_counter=$(($attempt_counter+1))
    sleep 2

done