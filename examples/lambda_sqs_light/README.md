# Lambda SQS Light
Template for build flexible SQS processor with AWS Lambda.

## Service Architecture
There is no diagram to describe it.

## Build environment script workflow
Example of the workflow to create the environment.
![Service-Stack](docs/runenv-workflow.drawio.png)

## General Service Routes Architecture
There are no routes for this project.

# Prerequisites
- Python 3.6 (Attention)
- docker
- docker-compose
- python-dotenv
- jsonformatter
- requests
- pytz
- redis
- pyyaml
- apispec
- marshmallow
- Flask

## Features
- Docker-compose 
- OpenApi
- SQS Integration
* Flask
* MySQL
* Redis

## Details about requirements files
### requirements.txt
Collection of common application modules, light modules.

### requirements.txt
Collection of specific application modules, heavy modules that can be converted to layers if necessary.

### requirements-tests.txt
Collection of specific test application modules.


## Installation

### Installing AWS CLI
Documentation:
https://docs.aws.amazon.com/pt_br/cli/latest/userguide/install-cliv2.html

Execute the follow command:
```
apt install python38-env
apt install awscli
apt install zip
app install pip
```
Execute the follow command:
```
aws configure
```
### Installing python venv support
Execute the follow command:
```
apt install python38-env
```

### Creating network
Execute the follow command:
```
./scripts/docker/create-network.sh
```

### Running via docker
Installing dependencies:
```
./scripts/venv.sh
```

To execute the build:
```
./scripts/runenv.sh --build
```

Execute the follow command:
```
./scripts/runenv.sh
```

### Running the app


[//]: # (```)

[//]: # (./scripts/localstack/lambda/invoke-sqs-function.sh lambda_sqs)

[//]: # (```)
Execute the follow command:
```
./scripts/localstack/sqs/send-message.sh
```
Execute the follow command to send specific file:
```
./scripts/localstack/sqs/send-message.sh test-queue ./samples/ocorens/cancelamento.json
```

## Samples
See the project samples in this folder [here](samples).

## Running tests
To run the unit tests of the project you can execute the follow command:

### Running creating the venv
To create the `venv` and install the modules execute:
```
./scripts/venv.sh
```

First you need install the tests requirements:
 ```
 ./scripts/venv-exec.sh ./scripts/tests/install-tests.sh 
 ```

 
### Unit tests:
Executing the tests:
 ```
./scripts/venv-exec.sh ./scripts/tests/unit-tests.sh
 ``` 
Executing a specific file:
 ```
./scripts/venv-exec.sh ./scripts/tests/unit-tests.sh /tests/unit/test_app.py
 ```
### Components tests:
Start the docker containers:
 ```
./scripts/testenv.sh
```

Executing the tests:
 ```
./scripts/venv-exec.sh ./scripts/tests/component-tests.sh
```
Executing a specific file:
 ```
./scripts/venv-exec.sh ./scripts/tests/component-tests.sh /tests/component/test_app.py
 ```
### Integration tests:
Copy the file `config/integration.env.example` to 
`config/integration.env` and edit it with de staging parameters.

Executing the tests:
 ```
./scripts/venv-exec.sh ./scripts/tests/integration-tests.sh
```
Executing a specific file:
```
./scripts/venv-exec.sh ./scripts/tests/integration-tests.sh /tests/integration/test_app.py
```

### All tests:
Executing the tests:
```
 ./scripts/venv-exec.sh ./scripts/tests/tests.sh 
 ```

## Generating coverage reports
To execute coverage tests you can execute the follow commands:

### Unit test coverage:
Execute the follow command:
``` 
./scripts/venv-exec.sh ./scripts/tests/unit-coverage.sh
``` 

### Component test coverage:
Start the docker containers:
``` 
./scripts/testenv.sh
```

Execute the follow command:
``` 
./scripts/venv-exec.sh ./scripts/tests/component-coverage.sh
```

### Integration test coverage:

Copy the file `config/integration.env.example` to 
`config/integration.env` and edit it with de staging parameters.

Execute the follow command:
``` 
./scripts/venv-exec.sh ./scripts/tests/integration-coverage.sh
```
> Observation:

The result can be found in the folder `target/*`.


## License
See the license [LICENSE.md](LICENSE.md).

## Contributions
* Anderson de Oliveira Contreira [andersoncontreira](https://github.com/andersoncontreira)

