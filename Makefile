
pyRun:=poetry run python main.py

run-ping:
	sudo $(pyRun) ping multi \
	    --host 1.1.1.1 \
	    --host 8.8.8.8 \
	    --host 114.114.114.114 \
	    --host 2.3.3.3 \
	    --host 36.36.36.36


run-speed-test-test:
	$(pyRun) speedtest test


run-speed-test-list:
	$(pyRun) speedtest list

run-traceroute:
	sudo $(pyRun) traceroute --host www.qq.com


run-test:
	sudo poetry run pytest vps_network


run-quick:export BENCH_APP_KEY=$(shell cat app_key.txt)
run-quick:
	rm -rf out_dir
	mkdir -p out_dir
	sudo -E poetry run python main.py quick --out-dir=out_dir


docker-build-release:
	docker build -f docker/Dockerfile       -t vps_bench_release:latest .

# release without vps_bench
docker-build-vps-network:
	docker build -f docker/vps_network.Dockerfile -t vps_bench_network:latest .

docker-build-nginx:
	docker build -f docker/nginx.Dockerfile -t vps_bench_nginx:latest    docker

docker-build-php:
	docker build -f docker/php.Dockerfile   -t vps_bench_php:latest      docker
