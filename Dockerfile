# syntax=docker/dockerfile:1
#FROM python:3.10-slim-buster
FROM balenalib/aarch64-alpine-python:latest
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "-m" , "main", "run"]