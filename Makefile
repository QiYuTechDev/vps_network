
run-ping:
	poetry run python vps_network ping \
	    --ip 1.1.1.1 \
	    --ip 8.8.8.8 \
	    --ip 114.114.114.114 \
	    --ip 2.3.3.3 \
	    --ip 36.36.36.36


run-speed-test:
	poetry run python vps_network speed-test


run-traceroute:
	sudo poetry run python vps_network traceroute --host www.qq.com --host www.linode.com
