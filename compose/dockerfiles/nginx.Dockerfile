FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY boilerplate-nginx.conf /etc/nginx/conf.d/
