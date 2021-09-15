# PHP 测试的是编译时间
FROM python:3.9

ARG PHP_VERSION=php-8.0.10

RUN apt update && apt install -y curl wget
RUN mkdir /php
WORKDIR /php
RUN wget https://www.php.net/distributions/${PHP_VERSION}.tar.gz
