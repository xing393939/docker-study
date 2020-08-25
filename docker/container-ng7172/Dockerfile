FROM nginx:1.15-alpine
COPY Dockerfile.nginx.conf /etc/nginx/conf.d/default.conf

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
&& apk update

# telnet
RUN apk add busybox-extras

EXPOSE 71
EXPOSE 72
EXPOSE 81
EXPOSE 82