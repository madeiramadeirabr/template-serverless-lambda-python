python3 -m venv venv
source ./venv/bin/activate

if [ "$1" = "--port" ]
then
  PORT=$2
fi
if [ -z "$PORT" ]
then
  PORT=5000
fi

# export FLASK_ENV=development
python3 -m uvicorn app:app --port $PORT