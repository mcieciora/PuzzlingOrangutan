FROM ubuntu:20.04

MAINTAINER mcieciora

RUN apt update; apt upgrade -y; apt install tox git pip -y

RUN git clone https://github.com/mcieciora/PuzzlingOrangutan.git /app

WORKDIR /app

RUN git checkout feature/pymongo_tdd_tests

RUN pip install -r requirements.txt