import xlrd

from aic_writer.adapter.interface import IExcelReader


class AreaInformationCityReader(IExcelReader):
    @staticmethod
    def get_data(excel_data: bytes) -> list[list[str]]:

        # ExcelデータからAreaInformationCityを取得する
        workbook = xlrd.open_workbook(file_contents=excel_data)

        # シートを選択
        worksheet = [s for s in workbook.sheets() if s.name == "AreaInformationCity"][0]

        # 各行からデータを取得する
        # AreaInformationCityは1,2列目だけ必要
        # また、３行目まではヘッダなので飛ばす
        data = [
            [worksheet.cell(row, 0).value, worksheet.cell(row, 1).value]
            for row in range(worksheet.nrows)
            if row >= 3
        ]
        return data
