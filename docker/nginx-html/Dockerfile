FROM nginx:1.15-alpine

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
&& apk update
RUN apk add busybox-extras && apk add curl

COPY Dockerfile.nginx.conf /etc/nginx/conf.d/default.conf
COPY . /code/

EXPOSE 80