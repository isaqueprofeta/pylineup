FROM python:3.6-alpine

RUN mkdir -p /pylineup/

ADD requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

WORKDIR /pylineup
