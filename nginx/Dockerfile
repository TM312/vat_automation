ARG NGINX_VERSION
# Defining the base image
FROM nginx:$NGINX_VERSION

WORKDIR /etc/nginx

RUN rm ./conf.d/default.conf
# Copy custom nginx config optimizations
COPY nginx.conf .
COPY ./dev/*.conf ./conf.d/dev.conf
