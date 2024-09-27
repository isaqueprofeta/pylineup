FROM python:3.11-alpine

RUN apk add --no-cache --virtual \
        .build-deps \
        gcc \
        g++ \
        musl-dev \
        python3-dev \
        cython \
        libffi-dev \
        tzdata

ENV TZ America/Sao_Paulo

ADD requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
RUN pip install --no-deps jsonpickle==3.3.0

RUN mkdir -p /pylineup/
RUN addgroup -S celery && adduser -S celery -G celery -u 1000
RUN chown -R celery:celery /pylineup

USER celery
WORKDIR /pylineup
