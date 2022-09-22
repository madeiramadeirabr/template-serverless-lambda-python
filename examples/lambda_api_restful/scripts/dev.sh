#!/bin/bash
export TEST_ENV=0
export DEV_MODE=1
if test -f ./scripts/preenv.sh; then
    source ./scripts/preenv.sh;
else
    echo './scripts/preenv.sh not found'
fi
docker-compose up $1 $2 $3
