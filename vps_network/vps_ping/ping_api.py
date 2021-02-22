from ..vps_api import NetworkApi

__all__ = ["PingApi"]


class PingApi(object):
    def __init__(self, network_api: NetworkApi):
        self._api = network_api
