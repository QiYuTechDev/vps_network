FROM python:3.9

ARG NGINX_VERSION="nginx-1.18.0"

RUN apt update && apt install -y curl wget
RUN mkdir /nginx
WORKDIR /nginx
RUN wget https://nginx.org/download/${NGINX_VERSION}.tar.gz
RUN tar -zxvf ${NGINX_VERSION}.tar.gz
WORKDIR /nginx/${NGINX_VERSION}
RUN ./configure
RUN make
RUN make install
###########################
# 安装目录
# /usr/local/nginx/
# 注意: 不支持 https
#
