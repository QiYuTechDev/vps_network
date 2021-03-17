# PHP 测试的是编译时间
FROM python:3.9

RUN apt update && apt install -y curl wget
RUN mkdir /php
WORKDIR /php
RUN wget https://www.php.net/distributions/php-8.0.3.tar.gz
