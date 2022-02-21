# syntax=docker/dockerfile:1
FROM python:3.10-slim-buster
WORKDIR /app
EXPOSE 80
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "main.py"]