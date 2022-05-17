# syntax=docker/dockerfile:1
FROM python:3.10-slim-buster
WORKDIR /reko
# setting up poetry
COPY pyproject.toml /reko
COPY poetry.lock /reko
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
#copying source files
COPY . .
#running bot
CMD [ "poetry", "run", "python", "main.py"]