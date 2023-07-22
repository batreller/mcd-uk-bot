from urllib.parse import urlparse

import aiohttp


class Proxy:
    def __init__(self, proxy: str = None, change_ip_url: str = None):
        self._proxy = proxy
        self._change_ip_url = change_ip_url
        self._proxy_scheme = urlparse(proxy).scheme

    async def change_ip(self) -> None:
        if self._change_ip_url is not None:
            async with aiohttp.ClientSession() as session:
                await session.get(self._change_ip_url)

    @property
    def proxy(self):
        return self._proxy
