FROM python:3.11.1-alpine3.17
MAINTAINER mcieciora

COPY ./src /app
COPY requirements.txt /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD [ "python3", "main.py" ]