# Gitlab docker builder image
# contemporary version of skopeo needed
FROM docker:20.10

ENV DOCKER_TLS_CERTDIR "/certs"

ENV DOCKER_CLI_EXPERIMENTAL enabled

ENV BUILDX_URL https://github.com/docker/buildx/releases/download/v0.8.2/buildx-v0.8.2.linux-amd64

RUN apk add --no-cache wget git bash findutils curl g++ libmagic skopeo jq

RUN apk add python3 python3-dev --repository=http://dl-cdn.alpinelinux.org/alpine/edge/main

RUN mkdir -p $HOME/.docker/cli-plugins/

RUN wget -q -O $HOME/.docker/cli-plugins/docker-buildx $BUILDX_URL

RUN chmod a+x $HOME/.docker/cli-plugins/docker-buildx

RUN python3 -m ensurepip

RUN rm -r /usr/lib/python*/ensurepip

RUN pip3 install --upgrade pip setuptools

RUN if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi

RUN if [ ! -e /usr/bin/python ]; then ln -sf /usr/bin/python3 /usr/bin/python; fi

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

COPY pyproject.toml /root/

WORKDIR /root

RUN . $HOME/.poetry/env && poetry config virtualenvs.create false && poetry install
