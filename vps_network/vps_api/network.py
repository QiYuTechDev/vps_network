import json
import logging
import platform
from threading import Thread
from typing import Optional, List

from requests import Session, Response

from .dt import (
    ServerListResp,
    ServerItem,
    ServerListForm,
    PingForm,
    SpeedForm,
    TraceForm,
    ReportResp,
)
from ..values import SERVER_URL

__all__ = ["NetworkApi"]


class NetworkApi(object):
    """
    VPS Network API

    :doc: https://vps.qiyutech.tech/api/docs
    """

    def __init__(
        self,
        app_key: Optional[str] = None,
        out_dir: Optional[str] = None,
        url: Optional[str] = None,
    ):
        """
        :param app_key: 访问的APPKey
        :param out_dir: 上报结果到目标目录
        :param url: 服务器URL
        """
        self._app_key: Optional[str] = app_key
        self._out_dir = out_dir
        self._url: str = SERVER_URL if url is None else url
        self._http: Session = Session()
        self._log = logging.getLogger("rich")

    def ping_report(self, form: PingForm) -> Optional[ReportResp]:
        self._report_to_file("ping.json", form.dict())

        url = f"{self._url}/ping"
        return self._do_report(url, form.dict())

    def speed_report(self, form: SpeedForm) -> Optional[ReportResp]:
        self._report_to_file("speed.json", form.dict())

        url = f"{self._url}/speed"
        return self._do_report(url, form.dict())

    def trace_report(self, form: TraceForm) -> Optional[ReportResp]:
        self._report_to_file("trace.json", form.dict())

        url = f"{self._url}/traceroute"
        return self._do_report(url, form.dict())

    def _report_to_file(self, file_name: str, data: dict):
        if self._out_dir is None:
            return
        out_file = f"{self._out_dir}/{file_name}"
        with open(out_file, "w") as fp:
            json.dump(data, fp, ensure_ascii=False)

    def _do_report(self, url: str, json_data: dict) -> Optional[ReportResp]:
        """
        执行上报数据

        :param url: 上报的URL
        :param json_data: 上报的数据
        """
        headers = {"Authorization": f"Bearer {self._app_key}"}
        resp = self._http.post(url, json=json_data, headers=headers, timeout=5)
        if resp.ok:
            self._log.info("上报 Ping 信息成功")
            return ReportResp(**resp.json())
        self._log.error(f"上报 Ping 信息失败: {resp=} {resp.content=}")
        return None

    def server_list(self, form: ServerListForm) -> List[ServerItem]:
        """
        获取服务器列表
        """
        url = f"{self._url}/server_list"
        resp = self._http.post(url, json=form.dict(), timeout=5)
        if resp.ok:
            ret = ServerListResp(**resp.json())
            return ret.servers
        return []

    def telemetry(self) -> Thread:
        """
        上报遥测数据
        """
        th = Thread(target=self.do_telemetry, name="telemetry")
        th.start()
        return th

    def do_telemetry(self) -> Response:
        """
        执行上报遥测数据
        """
        url = f"{self._url}/telemetry"
        j = {
            "info": {
                "os": platform.system(),
                "host": platform.node(),
                "os-ver": platform.release(),
                "processor": platform.processor(),
                "python": platform.python_version(),
            }
        }
        return self._http.post(url, json=j, timeout=5)
