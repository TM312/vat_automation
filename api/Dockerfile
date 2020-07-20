ARG PYTHON_VERSION
# Defining the base image
FROM python:$PYTHON_VERSION

# Set maintainer
LABEL maintainer="Thomas Moellers <thomas.moellers@unisg.ch>"

# Set the working directory
WORKDIR /home

RUN mkdir api && \
	mkdir data

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1 && \
	PYTHONUNBUFFERED 1
# install system dependencies
RUN apt-get update && apt-get install -y netcat

# Install the dependencies
COPY requirements.txt api/requirements.txt

RUN pip3 install --upgrade pip && \
	pip3 install --no-cache-dir -r api/requirements.txt && \
	pip3 install gunicorn

# copy project
WORKDIR /home/api
# COPY . api/.
COPY app app
COPY commands commands
COPY manage.py manage.py
COPY wsgi.py wsgi.py
COPY wait-for-it.sh wait-for-it.sh

WORKDIR /home
#copy data
COPY data data/

WORKDIR /home/api

# Add wait-for-it
RUN chmod +x wait-for-it.sh
