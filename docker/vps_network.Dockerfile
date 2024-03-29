# Use Docker Multi Stage Build

########################################
# Rust Build Docker Image
FROM python:3.9 as BASE

# install poetry
COPY . /app
WORKDIR /app
RUN pip install poetry && poetry build


########################################
# nginx 镜像
FROM python:3.9 as NGINX

RUN apt update && apt install -y curl wget
RUN mkdir /nginx
WORKDIR /nginx
RUN wget -q https://nginx.org/download/nginx-1.18.0.tar.gz
RUN tar -zxvf nginx-1.18.0.tar.gz
WORKDIR /nginx/nginx-1.18.0
RUN ./configure
RUN make
RUN make install
###########################
# 安装目录
# /usr/local/nginx/
# 注意: 不支持 https
#


########################################
# php 测试镜像
FROM python:3.9 as PHP

ARG PHP_VERSION="php-8.0.10"

RUN apt update && apt install -y curl wget
RUN mkdir /php
WORKDIR /php
RUN -q wget https://www.php.net/distributions/${PHP_VERSION}.tar.gz


########################################
# 最终的镜像
FROM python:3.9

MAINTAINER dev@qiyutech.tech

ARG PHP_VERSION="php-8.0.10"

# copy vps_bench to bin dir
COPY --from=BASE  /app/dist/*                               /app/dist/
COPY --from=NGINX /usr/local/nginx                          /user/local
COPY --from=PHP   /php/${PHP_VERSION}.tar.gz                /php/
COPY              ./scripts/php.bash                        /php/php.bash

# 我们测试的 PHP 版本
ENV PHP_VERSION="8.0.10"

# install the vps_network dep
# this version num may be need change from time to time
RUN pip install --no-cache-dir /app/dist/vps_network-0.7.0-py3-none-any.whl

COPY main.py /bin/vps_network
RUN chmod a+x            \
        /bin/vps_network \
        /php/php.bash
