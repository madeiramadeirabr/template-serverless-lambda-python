#!/bin/bash
echo 'Validating jd installation..'
  /usr/bin/jq --help > /dev/null 2>&1
  if [ $? -ne 0 ]; then
    echo 'Installing'
    # download directly into ~/bin_compciv
    sudo curl http://stedolan.github.io/jq/download/linux64/jq -o /usr/bin/jq
    # give it executable permissions
    sudo chmod a+x /usr/bin/jq
  fi

echo 'Validate connection'
./scripts/boot-validate-connection.sh

echo 'Create the queues...'
./scripts/boot-queues.sh

echo 'Create the lambdas...'
./scripts/boot-lambdas.sh