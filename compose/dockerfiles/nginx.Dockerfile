FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY wallet-nginx.conf /etc/nginx/conf.d/
