import requests

from aic_writer.adapter.interface import IClient


class HTTPClient(IClient):
    """
    respという知識を外に出さないようにstr or binで関数を分けている
    """

    @staticmethod
    def _get(url: str) -> requests.Response:
        resp = requests.get(url=url)

        # 200以外の場合は例外
        resp.raise_for_status()

        return resp

    def get_as_str(self, url: str) -> str:
        with self._get(url) as resp:
            result = resp.text
        return result

    def get_as_bin(self, url: str) -> bytes:
        with self._get(url) as resp:
            result = resp.content
        return result
