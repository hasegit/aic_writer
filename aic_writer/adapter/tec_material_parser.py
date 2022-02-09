"""気象庁技術資料を検索"""

import re
from dataclasses import dataclass
from typing import Final

from bs4 import BeautifulSoup

from aic_writer.usecase.interface import IParser


@dataclass
class TecMaterialParser(IParser):

    CODE_FILE: Final[re.Pattern] = re.compile(r"jmaxml_\d{8}_Code.zip")

    def parse(self, html: str) -> str:
        """
        気象庁技術資料ページデータからコード一覧のデータを特定する
        """
        # htmlをパースしてコード一覧を特定する
        soup = BeautifulSoup(html, features="html5lib")
        for atag in soup.find_all("a"):
            href = atag.get("href")
            if not href:
                continue
            if self.CODE_FILE.match(href):
                return href

        return ""
