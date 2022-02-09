"""ユースケース
・気象庁の技術資料ホームページを開く
・その中からコード一覧を探す
・コード一覧をダウンロードする
・コード一覧をExcelで開く
・使いやすいデータ(ドメインオブジェクト)にする
・DBにデータを登録する
"""

from dataclasses import dataclass

from aic_writer.domain import AreaInformationCityList

from .interface import IParser, ReadRepository, WriteRepository


@dataclass
class AICInteractor:
    """AreaInformationCityInteractor"""

    read_repository: ReadRepository
    write_repository: WriteRepository
    parser: IParser

    def handle(self):

        # 技術資料データを取得
        html = self.read_repository.get_tec_material_page()

        # パースしてコード一覧のzipファイルを特定
        target = self.parser.parse(html)

        # コード一覧をダウンロードしてデータを抽出
        code_list: AreaInformationCityList = self.read_repository.get_code_list(target)

        # データをJSON化
        code_list_dict: list[dict[str, str]] = code_list.as_dict()

        # dbに登録
        self.write_repository.update(code_list_dict)
