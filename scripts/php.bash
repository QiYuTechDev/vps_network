#!/usr/bin/env bash

set -e

pushd /php # push 1

# 解压 PHP 源代码
tar -zxvf php-8.0.3.tar.gz

# 进入 PHP 目录
pushd /php/php-8.0.3 # push 2
./configure

# 编译 PHP
make

popd # pop 2

# 清理编译产出
rm -rf php-8.0.3

popd # pop 1
