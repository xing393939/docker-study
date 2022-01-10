FROM node:alpine3.10

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
&& apk update
RUN apk add busybox-extras && apk add curl

ADD app.js /app.js
ENTRYPOINT ["node", "app.js"]
