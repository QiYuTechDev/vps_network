import statistics
from typing import List, Optional

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


@main.command()
@click.option(
    "--server",
    multiple=True,
    help="期望使用的 SpeedTest 目标服务器, 注意: 这个值是 SpeedTest 测试服务器的 ID",
)
@click.option(
    "--disable",
    type=click.Choice(["up", "dl"], case_sensitive=False),
    help="禁止 上传/下载 测试, 不允许同时禁止",
)
@click.option(
    "--up-threads",
    type=int,
    help="上传线程数量",
)
@click.option(
    "--dl-threads",
    type=int,
    help="下载线程数量",
)
def speed_test(
    server: Optional[List[str]],
    disable: Optional[str],
    up_threads: Optional[int],
    dl_threads: Optional[int],
):
    """
    网络速度测试

    服务器列表 ID 可以尝试从这儿获取: https://williamyaps.github.io/wlmjavascript/servercli.html
    """
    from vps_speedtest import do_speed_test

    from rich.table import Table
    from rich.console import Console

    console = Console()

    ret = do_speed_test(
        servers=server, disable=disable, dl_threads=dl_threads, up_threads=up_threads
    )

    server = ret.server
    table = Table(title="服务器信息")
    table.add_column("字段")
    table.add_column("值")
    table.add_row("ID", server.id)
    table.add_row("HOST", server.host)
    table.add_row("URL", server.url)
    table.add_row("经度", server.lat)
    table.add_row("纬度", server.lon)
    table.add_row("名称", server.name)
    table.add_row("国家", server.country)
    table.add_row("延迟", str(server.latency))
    table.add_row("赞助商", server.sponsor)
    console.print(table)

    client = ret.client
    table = Table(title="客户端信息")
    table.add_column("字段")
    table.add_column("值")
    table.add_row("IP", client.ip)
    table.add_row("经度", client.lat)
    table.add_row("纬度", client.lon)
    table.add_row("ISP", client.isp)
    table.add_row("国家", client.country)
    console.print(table)

    table = Table(title="SpeedTest 结果")
    table.add_column("字段")
    table.add_column("值")
    table.add_row("下载速度", f"{ret.download:.2f}")
    table.add_row("上传速度", f"{ret.upload:.2f}")
    table.add_row("Ping", f"{ret.ping:.2f}")
    table.add_row("时间", ret.timestamp)
    table.add_row("发送数据量", f"{ret.bytes_send}")
    table.add_row("接收数据量", f"{ret.bytes_received}")
    console.print(table)


@main.command()
@click.option("--host", multiple=True, required=True, help="目标服务器")
@click.option("--count", type=int, default=2, help="每个IP地址发送多少个Ping请求")
@click.option("--hops", type=int, default=32, help="最多多少跳(TCP time to live)")
@click.option("--fast", is_flag=True, help="快速模式")
def traceroute(host: List[str], count: int, hops: int, fast: bool):
    """
    traceroute [host]

    traceroute 目的主机测试

    注意: 这个程序需要使用 Root 运行
    """
    from rich.console import Console
    from rich.table import Table
    from rich.live import Live
    from vps_traceroute import do_traceroute

    console = Console()

    for addr in host:
        table = Table(title=f"Traceroute ({addr}) 测试", show_lines=True)
        table.add_column("IP", justify="right")
        table.add_column("位置", justify="right")
        table.add_column("ISP", justify="right")
        table.add_column("最小RTT", justify="right")
        table.add_column("平均RTT", justify="right")
        table.add_column("最大RTT", justify="right")

        with Live(
            table,
            console=console,
            refresh_per_second=8,
            transient=True,
            vertical_overflow="visible",
        ):
            result = do_traceroute(
                table=table, address=addr, count=count, max_hops=hops, fast=fast
            )
            print(result)
        print("\n" * 60)
        console.clear()
        console.print(table)


@main.command()
@click.option("--ip", multiple=True, help="目的服务器IP, 允许多个值")
@click.option("--no-telemetry", is_flag=True, help="关闭遥测数据", hidden=True)
def ping(ip: List[str], no_telemetry: bool):
    """
    ping 测试
    """
    from vps_ping import do_multi_ping
    from rich.console import Console
    from rich.table import Table

    results = do_multi_ping(ip)

    table = Table(title="Ping 测试结果 (时间单位: ms)")
    table.add_column("IP", justify="right", style="cyan", no_wrap=True)
    table.add_column("最小RTT")
    table.add_column("最大RTT")
    table.add_column("平均RTT")
    table.add_column("标准差")
    table.add_column("失败", style="red")
    table.add_column("成功", style="green")

    for ret in results:
        success = list(filter(lambda x: x is not None, ret.times))
        if len(success) == 0:
            success = [0, 0]

        failure = len(list(filter(lambda x: x is None, ret.times)))
        row = [
            ret.host,
            f"{min(success):.2f}",
            f"{max(success):.2f}",
            f"{statistics.mean(success):.2f}",
            f"{statistics.stdev(success):.2f}",
            str(failure),
            str(len(ret.times) - failure),
        ]
        table.add_row(*row)

    console = Console()
    console.print(table)


if __name__ == "__main__":
    main()
