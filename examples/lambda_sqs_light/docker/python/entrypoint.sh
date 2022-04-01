#!/bin/bash
# aws configure for localstack
aws configure set region us-east-1 --profile default

# define the environment variable indicating thar are running inside a container
#!/bin/bash
if [ -f /.dockerenv ]; then
    echo "I'm inside matrix ;(";
    export RUNNING_IN_CONTAINER=1
else
    echo "I'm living in real world!";
    export RUNNING_IN_CONTAINER=0
fi

#echo $RUNNING_IN_CONTAINER

# execute the boot.sh
bash ./scripts/boot.sh

# execute the flask
# flask run --host 0.0.0.0
python3 server.py