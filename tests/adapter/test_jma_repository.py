import zipfile

from aic_writer.adapter import IClient, IExcelReader, JMARepository
from aic_writer.domain import AreaInformationCity, AreaInformationCityList


class MockClient(IClient):
    @staticmethod
    def get_as_str(_: str) -> str:
        return "OK"

    @staticmethod
    def get_as_bin(_: str):
        with open("tests/data/jmaxml_20220222_Code.zip", "rb") as zip_file:
            data = zip_file.read()
        return data


class MockReader(IExcelReader):
    @staticmethod
    def get_data(excel_data: bytes) -> list[list[str]]:
        return [["99999999", "ほげ県ふが町"]]


class TestJMARepository:
    @staticmethod
    def test_get_tec_material_page():
        # 自身の持つClientが実行されているかだけをチェック
        repository = JMARepository(MockClient(), MockReader())
        result = repository.get_tec_material_page()
        assert result == "OK"

    @staticmethod
    def test_get_code_list():
        repository = JMARepository(MockClient(), MockReader())
        result = repository.get_code_list("hoge")
        assert result == AreaInformationCityList([AreaInformationCity("99999999", "ほげ県ふが町")])
