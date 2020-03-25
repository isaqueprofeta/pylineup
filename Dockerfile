FROM python:3.6-alpine

RUN apk add --no-cache tzdata
ENV TZ America/Sao_Paulo

ADD requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /pylineup/
WORKDIR /pylineup
