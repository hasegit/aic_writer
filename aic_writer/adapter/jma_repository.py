"""Japan Meteorological Agency Repository"""

import re
import zipfile
from dataclasses import dataclass
from io import BytesIO
from typing import Final
from urllib.parse import ParseResult, urlparse

from aic_writer.domain import AreaInformationCity, AreaInformationCityList
from aic_writer.usecase.interface import ReadRepository

from . import IClient, IExcelReader


@dataclass
class JMARepository(ReadRepository):
    """JMAの知識はここに閉じ込めておく"""

    client: IClient
    reader: IExcelReader
    URL: Final[ParseResult] = urlparse("http://xml.kishou.go.jp/tec_material.html")
    XLS_NAME: Final[re.Pattern] = re.compile(r"\d{8}_AreaInformationCity-AreaForecastLocalM.xls")

    def get_tec_material_page(self) -> str:
        """
        気象庁技術資料ページを取得する
        """
        return self.client.get_as_str(self.URL.geturl())

    def get_code_list(self, target: str) -> AreaInformationCityList:
        """
        気象庁技術資料ページのコード一覧のzipを取得し、
        中からExcelを抽出した上でデータを取得する
        """
        # zipデータの取得
        xls_data: bytes = self._download_zip(target)

        # ExcelデータからAreaInformationCityを抽出
        aic_data: list[list[str]] = self.reader.get_data(xls_data)

        # ValueObjectに詰め込み返却する
        # このとき、Excelから取得したコードが数値扱いされているので、int/strで綺麗にする
        return AreaInformationCityList(
            [AreaInformationCity(code=str(int(d[0])), area=d[1]) for d in aic_data]
        )

    def _download_zip(self, target: str) -> bytes:
        # zipデータの取得
        url = f"{self.URL.scheme}://{self.URL.netloc}/{target}"
        zip_data = self.client.get_as_bin(url)

        # zipデータを開く
        with zipfile.ZipFile(BytesIO(zip_data)) as zip_file:

            # zipデータからyyyymmdd_AreaInformationCity-AreaForecastLocalM.xlsを探す
            target_file: str = ""
            for filename in zip_file.namelist():
                if self.XLS_NAME.match(filename):
                    target_file = filename
                    break

            # もしファイルが見つからなかった場合は何もしない
            if not target_file:
                print("Cannot find")
                return bytes()

            # zipからExcelデータを抽出
            return zip_file.read(target_file)
