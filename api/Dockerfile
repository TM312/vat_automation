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

# # The RUN chmod command ensures that this new boot.sh file can be executed by anyone (+x)
RUN chmod +x ./entrypoint.sh

# # USER tm

ENTRYPOINT ["./entrypoint.sh"]
