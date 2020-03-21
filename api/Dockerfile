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

# Install the dependencies
COPY requirements.txt /usr/src/app/requirements.txt
# COPY requirements.txt requirements.txt
# RUN venv/bin/pip install --upgrade pip && \
# 	venv/bin/pip install --no-cache-dir -r requirements.txt && \
# 	venv/bin/pip install gunicorn

RUN pip3 install --upgrade pip && \
	pip3 install --no-cache-dir -r requirements.txt && \
	pip3 install gunicorn

# copy project
COPY . /usr/src/app/
# COPY app app
# COPY migrations migrations
# COPY commands commands
# COPY manage.py boot.sh wsgi.py ./

# The RUN chmod command ensures that this new boot.sh file can be executed by anyone (+x)
# RUN chmod +x ./boot.sh

# USER tm

# ENTRYPOINT ["./boot.sh"]

ENTRYPOINT ["gunicorn"]
CMD ['-w', '1', 'wsgi:app']
# CMD [ "wsgi.py" ]
