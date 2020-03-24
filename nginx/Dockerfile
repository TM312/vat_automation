FROM nginx:1.15

RUN rm /etc/nginx/conf.d/default.conf
# Copy custom nginx config optimizations
COPY ./nginx.conf /etc/nginx/nginx.conf
