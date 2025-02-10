FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN p3p -nstall --upgrade setuptools
RUN pip3 install --no-cache-dir -r requirements.txt
RUN chmod 755 .
COPY . .

