#!/usr/bin/env python3

import click


@click.group("main")
@click.version_option("v0.1.0")
def main():
    """
    VPS 网络测试工具箱

    报告错误: https://github.com/QiYuTechDev/vps_network

    版权所有: 奇遇科技
    """
    pass


from vps_network.vps_speed import init_speed_test_cli
from vps_network.vps_ping import init_ping_cli
from vps_network.vps_trace import init_traceroute_cli
from vps_network.vps_quick import init_quick_cli

init_speed_test_cli(main)
init_ping_cli(main)
init_traceroute_cli(main)
init_quick_cli(main)

if __name__ == "__main__":
    main()
