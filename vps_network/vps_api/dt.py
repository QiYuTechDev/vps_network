from typing import List, Optional

from pydantic import BaseModel, Field

from ..vps_ping import PingResult
from ..vps_speed import SpeedTestResult
from ..vps_trace import TraceResult

__all__ = [
    "ServerListResp",
    "ServerItem",
    "ServerListForm",
    "PingForm",
    "SpeedForm",
    "TraceForm",
]


class ServerItem(BaseModel):
    name: str = Field(..., title="服务器名称")
    country: str = Field(..., title="国家")
    speed_test_id: Optional[int] = Field(None, title="SpeedTest ID")
    host: str = Field(..., title="服务器地址")

    def __init__(self, **kwargs):
        country = kwargs.get("country", None)
        # this is a workaround for server site
        if not isinstance(country, str):
            kwargs["country"] = str(country)
        super().__init__(**kwargs)


class ServerListResp(BaseModel):
    servers: Optional[List[ServerItem]] = Field(..., title="服务器列表")


class ServerListForm(BaseModel):
    cc: Optional[str] = Field(None, title="国家", description="服务器所在的过滤")
    limit: int = Field(32, title="获取多少个数据")


class ReportBaseForm(BaseModel):
    job_id: Optional[str] = Field(None, title="任务ID", description="如果使用 快速 测试则有 任务 ID")


class PingForm(ReportBaseForm):
    results: List[PingResult] = Field(..., title="Ping测试结果")


class SpeedForm(ReportBaseForm):
    results: List[SpeedTestResult] = Field(..., title="网络速度测试结果")


class TraceForm(ReportBaseForm):
    results: List[TraceResult] = Field(..., title="网络跟踪测试结果")
