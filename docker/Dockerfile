# Use Docker Multi Stage Build

FROM python:3.9 as BASE

# 安装 git
RUN apt update && apt install -y git

# install rust
RUN apt update && apt install -y curl
RUN curl --proto '=https' -sSf https://sh.rustup.rs | sh -s -- --default-toolchain none -y
ENV PATH="/root/.cargo/bin:${PATH}"
RUN rustup toolchain install stable --allow-downgrade --profile minimal
RUN apt install -y gcc

RUN mkdir /build
WORKDIR /build

# download & build VPS Bench 工具
RUN git clone https://github.com/QiYuTechDev/vps_bench

RUN cd /build/vps_bench && cargo build --release

# install poetry
COPY . /app
WORKDIR /app
RUN pip install poetry && poetry build

# second
FROM python:3.9

MAINTAINER dev@qiyutech.tech

# copy vps_bench to bin dir
COPY --from=BASE /build/vps_bench/target/release/vps_bench /bin/
COPY --from=BASE /app/dist/* /app/dist/

# install the vps_network dep
# this version num may be need change from time to time
# or we publish vps_network to pypi???
RUN pip install --no-cache-dir /app/dist/vps_network-0.2.6-py3-none-any.whl

COPY main.py /bin/vps_network
RUN chmod a+x /bin/vps_network
