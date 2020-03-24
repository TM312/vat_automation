ARG POSTGRES_VERSION
# Defining the base image
FROM postgres:$POSTGRES_VERSION

ADD create.sql /docker-entrypoint-initdb.d
