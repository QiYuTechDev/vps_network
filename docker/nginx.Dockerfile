FROM python:3.9

# view nginx download url:
# https://nginx.org/en/download.html
ARG NGINX_VERSION="nginx-1.20.1"

RUN apt update && apt install -y curl wget
RUN mkdir /nginx
WORKDIR /nginx
RUN wget -q https://nginx.org/download/${NGINX_VERSION}.tar.gz
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
