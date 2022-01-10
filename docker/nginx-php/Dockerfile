FROM nginx

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
&& apk update
RUN apk add busybox-extras && apk add curl

COPY src/ /code/
COPY default.conf /etc/nginx/conf.d/default.conf

EXPOSE 70
