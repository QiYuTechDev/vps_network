#!/usr/bin/env bash

set -e

pushd /php # push 1

# view php version on: https://www.php.net/

export PHP_VERSION=php-8.0.10

# 解压 PHP 源代码
tar -zxvf ${PHP_VERSION}.tar.gz

# 进入 PHP 目录
pushd /php/${PHP_VERSION} # push 2
./configure

# 编译 PHP
make

popd # pop 2

# 清理编译产出
rm -rf ${PHP_VERSION}

popd # pop 1
