FROM nginx:1.15-alpine

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
&& apk update

# telnet
RUN apk add busybox-extras

COPY Dockerfile.nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 71
EXPOSE 72
EXPOSE 91
EXPOSE 92