
pyRun:=poetry run python main.py

run-ping:
	sudo $(pyRun) ping \
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
	sudo $(pyRun) traceroute --host www.qq.com --host www.linode.com


run-test:
	sudo poetry run pytest vps_network
