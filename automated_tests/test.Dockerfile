FROM python:3.11.1-alpine3.17
MAINTAINER mcieciora

COPY ./automated_tests /app/automated_tests
COPY ./src /app/src
COPY requirements.txt /app
WORKDIR /app

RUN python3.11 -m pip install -r requirements.txt
RUN python3.11 -m pip install -r automated_tests/requirements.txt

ENTRYPOINT [ "python3.11" ]