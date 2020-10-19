FROM php:7.3-fpm-alpine3.12
WORKDIR /code
RUN chown -R www-data:www-data /code

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
&& apk update

# telnet
RUN apk add busybox-extras

# timezone
RUN printf '[PHP]\ndate.timezone = "Asia/Shanghai"\n' > /usr/local/etc/php/conf.d/timezone.ini

# pdo_mysql
RUN docker-php-ext-install pdo_mysql

# redis不是php-src里的，因此不能使用docker-php-ext-install
RUN apk add --no-cache --update --virtual .phpize-deps $PHPIZE_DEPS \
    && pecl install -o -f redis-5.0.0 && docker-php-ext-enable redis

# gd
RUN apk add --no-cache freetype libpng libjpeg-turbo freetype-dev libpng-dev libjpeg-turbo-dev && \
docker-php-ext-configure gd \
--with-gd \
--with-freetype-dir=/usr/include/ \
--with-png-dir=/usr/include/ \
--with-jpeg-dir=/usr/include/ && \
NPROC=$(grep -c ^processor /proc/cpuinfo 2>/dev/null || 1) && \
docker-php-ext-install -j${NPROC} gd

# mcrypt
RUN apk add --no-cache libmcrypt-dev \
&& pecl install mcrypt-1.0.2 \
&& docker-php-ext-enable mcrypt

# OPcache defaults
RUN docker-php-ext-configure opcache --enable-opcache && docker-php-ext-install opcache
ENV PHP_OPCACHE_ENABLE="1"
ENV PHP_OPCACHE_MEMORY_CONSUMPTION="128"
ENV PHP_OPCACHE_MAX_ACCELERATED_FILES="10000"
ENV PHP_OPCACHE_REVALIDATE_FREQUENCY="0"
ENV PHP_OPCACHE_VALIDATE_TIMESTAMPS="0"

# PHP-FPM defaults
RUN tmp=/usr/local/etc/php-fpm.d/www.conf \
&& sed -i 's/pm.max_children/pm.max_children=50 ;/' $tmp \
&& sed -i 's/pm.start_servers/pm.start_servers=20 ;/' $tmp \
&& sed -i 's/pm.max_spare_servers/pm.max_spare_servers=20 ;/' $tmp


EXPOSE 9000

