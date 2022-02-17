FROM python:3.8.11-alpine3.13
MAINTAINER Anderson Contreira <anderson.contreira@gmail.com>

ARG FLASK_PORT=5000
ARG ENVIRONMENT_NAME=development
ENV FLASK_ENV=$ENVIRONMENT_NAME \
    FLASK_APP=app.py

EXPOSE ${FLASK_PORT}

WORKDIR /app

# SQLite support
RUN apk update \
    && apk add sqlite \
    && apk add socat

# gcc requirement for greenlit and sqlalchemy
RUN apk add --no-cache build-base \
                       python3-dev \
                       libffi-dev \
                       musl-dev \
                       make \
                       gcc \
                       openldap \
                       libcurl \
                       gpgme-dev \
                       libc-dev \
                       bash \
                       curl \
                       zip \
    && rm -rf /var/cache/apk/*

# upgrade pip
RUN pip install --upgrade pip

# install aws cli
RUN pip --no-cache-dir install --upgrade awscli

RUN rm -Rf ./vendor/*

# Install requirements
COPY requirements.txt requirements-vendor.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r requirements-vendor.txt

# Flask compatibility with Python 3.8
RUN pip uninstall dataclasses -y
RUN rm -Rf ./vendor/dataclasses-0.8.dist-info/ ./vendor/dataclasses.py

# Copy project files
COPY . .

# entrypoint permission
RUN ["chmod", "+x", "./docker/python/entrypoint.sh"]
# entrypoint
ENTRYPOINT ["sh", "./docker/python/entrypoint.sh"]

CMD [ "flask", "run", "--host", "0.0.0.0" ]

