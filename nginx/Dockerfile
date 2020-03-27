ARG NGINX_VERSION
# Defining the base image
FROM nginx:$NGINX_VERSION

#RUN rm /etc/nginx/conf.d/default.conf
# Copy custom nginx config optimizations
COPY ./nginx.conf /etc/nginx/nginx.conf
#COPY ./dev/local_deploy.conf /etc/nginx/conf.d/local_deploy.conf
