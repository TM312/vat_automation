ARG PYTHON_VERSION
# ARG USER_ID
# ARG GROUP_ID

# Defining the base image
FROM python:$PYTHON_VERSION

# RUN echo "The User ID is really: $USER_ID"
# RUN echo "The Group ID is really: $GROUP_ID"
# RUN echo "The PYTHON_VERSION is really: $PYTHON_VERSION"

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
RUN apt-get update && apt-get install -y \
	netcat \
	gcc \
	musl-dev \
	curl

# Install the dependencies
COPY requirements.txt api/requirements.txt

RUN pip3 install --upgrade pip  \
	&& pip3 install --no-cache-dir -r api/requirements.txt \
	&& pip3 install gunicorn \
	&& pip3 install --no-cache-dir cython


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

# RUN addgroup --gid 1237 tm
# RUN adduser --disabled-password --gecos '' --uid 10239 --gid 1237 tm
# USER tm
