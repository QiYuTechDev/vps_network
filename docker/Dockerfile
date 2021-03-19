# Use Docker Multi Stage Build

########################################
# Rust Build Docker Image
FROM python:3.9 as BASE

# 安装 git
RUN apt update && apt install -y git

# install rust
RUN apt update && apt install -y curl
RUN curl --proto '=https' -sSf https://sh.rustup.rs | sh -s -- --default-toolchain none -y
ENV PATH="/root/.cargo/bin:${PATH}"
RUN rustup toolchain install stable --allow-downgrade --profile minimal
RUN apt install -y gcc libssl-dev

RUN mkdir /build
WORKDIR /build

# download & build VPS Bench 工具
RUN git clone https://github.com/QiYuTechDev/vps_bench

RUN cd /build/vps_bench && cargo build --release

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
RUN wget https://nginx.org/download/nginx-1.18.0.tar.gz
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

RUN apt update && apt install -y curl wget
RUN mkdir /php
WORKDIR /php
RUN wget https://www.php.net/distributions/php-8.0.3.tar.gz


########################################
# 最终的镜像
FROM python:3.9

MAINTAINER dev@qiyutech.tech

# copy vps_bench to bin dir
COPY --from=BASE  /build/vps_bench/target/release/vps_bench /bin/
COPY --from=BASE  /app/dist/*                               /app/dist/
COPY --from=NGINX /usr/local/nginx                          /user/local
COPY --from=PHP   /php/php-8.0.3.tar.gz                     /php/
COPY              ./scripts/php.bash                        /php/php.bash

# 我们测试的 PHP 版本
ENV PHP_VERSION 8.0.3

# install the vps_network dep
# this version num may be need change from time to time
RUN pip install --no-cache-dir /app/dist/vps_network-0.4.0-py3-none-any.whl

COPY main.py /bin/vps_network
RUN chmod a+x            \
        /bin/vps_network \
        /php/php.bash
