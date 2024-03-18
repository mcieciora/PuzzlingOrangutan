FROM python:3.12.1-slim

WORKDIR /app
COPY requirements.txt requirements/requirements-testing.txt pytest.ini ./

WORKDIR /app/automated_tests
COPY automated_tests .

WORKDIR /app/src
COPY src .

WORKDIR /app
RUN python3 -m pip install --no-cache-dir -r requirements.txt -r requirements-testing.txt