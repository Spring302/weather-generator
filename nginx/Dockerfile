FROM nginx:latest

RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/
RUN rm -f /etc/nginx/conf.d/default.conf
COPY project.conf /etc/nginx/conf.d/