# Defining the base image
ARG NGINX_VERSION
FROM nginx:$NGINX_VERSION

WORKDIR /etc/nginx

RUN rm ./conf.d/default.conf
# Copy custom nginx config optimizations
COPY nginx.conf .
# https://docs.docker.com/engine/reference/builder/#understand-how-arg-and-from-interact
ARG ENVIRONMENT
COPY ./${ENVIRONMENT}/*.conf ./conf.d/
