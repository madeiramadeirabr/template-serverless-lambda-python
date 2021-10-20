# template-serverless-lambda-python - Lambda SQS
Template for build flexible SQS processor with AWS Lambda.

## Service Architecture
Example of architecture with AWS SQS and AWS Lambda.
![Service-Arch](docs/service-arch.png)

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

## Installation

### Installing AWS CLI
Documentation:
https://docs.aws.amazon.com/pt_br/cli/latest/userguide/install-cliv2.html

Execute the follow command:
```
apt install awscli
apt install zip
app install pip
```
Execute the follow command:
```
aws configure
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

### Boot the lambda
Execute the follow command:
```
./scripts/boot.sh
```

### Running the app
Execute the follow command:
```
./scripts/localstack/lambda/invoke-sqs-function.sh lambda_sqs
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
 ```
./scripts/venv-exec.sh ./scripts/tests/unit-tests.sh
 ``` 
### Components tests:
Start the docker containers:
 ```
./scripts/runenv.sh
```
Booting the environment:
 ```
./scripts/boot.sh
```

Executing the tests:
 ```
./scripts/venv-exec.sh ./scripts/tests/component-tests.sh
```
### Integration tests:
Copy the file `config/integration.env.example` to 
`config/integration.env` and edit it with de staging parameters.

Executing the tests:
 ```
./scripts/venv-exec.sh ./scripts/tests/integration-tests.sh
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
./scripts/runenv.sh
```
Booting the environment:
 ```
./scripts/boot.sh
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

