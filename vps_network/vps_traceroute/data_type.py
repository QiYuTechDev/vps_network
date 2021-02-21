from typing import Optional, List

from pydantic import Field, BaseModel

__all__ = ["TraceHop", "TraceResult"]


class TraceHop(BaseModel):
    ip: str = Field(..., title="IP地址")
    # rtt times
    times: List[Optional[float]] = Field(..., title="RTT时间", description="没有则表示没有收到回复")
    # any other ip information
    info: Optional[dict] = Field(None, title="其他信息")


class TraceResult(BaseModel):
    results: List[Optional[TraceHop]] = Field(..., title="Trace结果")
