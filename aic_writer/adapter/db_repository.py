"""
DB Repository
データをDB用に変換する
今回は変換不要
"""

from dataclasses import dataclass

from aic_writer.usecase import WriteRepository

from .interface import DBDriver


@dataclass
class DBRepository(WriteRepository):

    driver: DBDriver

    def update(self, data: list[dict[str, str]]):
        """
        データをDBに入れる
        updateとはいうものの、コードの統廃合の可能性もあるので
        実際はdelete table -> create table -> create itemとなる
        """
        self.driver.delete_table()
        self.driver.create_table()
        self.driver.create_data(data)
