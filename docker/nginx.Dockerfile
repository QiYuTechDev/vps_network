FROM python:3.9

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
