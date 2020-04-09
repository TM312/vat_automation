ARG PYTHON_VERSION
# Defining the base image
FROM python:$PYTHON_VERSION

# Set maintainer
LABEL maintainer="Thomas Moellers <thomas.moellers@unisg.ch>"

# Set the working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1 && \
	PYTHONUNBUFFERED 1
# install system dependencies
RUN apt-get update && apt-get install -y netcat

# Install the dependencies
COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip && \
	pip3 install --no-cache-dir -r requirements.txt && \
	pip3 install gunicorn

# copy project
COPY . .

# Add wait-for-it
RUN chmod +x wait-for-it.sh
