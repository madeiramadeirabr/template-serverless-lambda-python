if test -f .projectrc; then
  source .projectrc
elif test -f ./bin/.projectrc; then
  source ./bin/.projectrc
fi

if [ -z "$NETWORK_NAME" ]; then
  echo 'NETWORK_NAME not defined'
  exit 1
else
  docker network create $NETWORK_NAME
fi
