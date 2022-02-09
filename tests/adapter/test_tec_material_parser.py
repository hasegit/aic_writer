import pytest

from aic_writer.adapter import TecMaterialParser


class TestTecMaterialParser:
    @staticmethod
    @pytest.mark.parametrize(
        "data,expected",
        [
            ["<a></a>", ""],
            ['<a href="hoge"></a>', ""],
            [
                '<a href="hoge"></a><a href="jmaxml_20220222_Code.zip"></a>',
                "jmaxml_20220222_Code.zip",
            ],
        ],
    )
    def test_parse(data, expected):

        parser = TecMaterialParser()
        result = parser.parse(data)
        assert result == expected
