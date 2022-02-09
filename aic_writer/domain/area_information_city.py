import json
from dataclasses import dataclass


@dataclass
class AreaInformationCity:
    code: str
    area: str


@dataclass
class AreaInformationCityList:
    data: list[AreaInformationCity]

    # 与えられたコードから地域を返す
    def search_area(self, code: str) -> str:
        for datum in self.data:
            if datum.code == code:
                return datum.area
        return ""

    # dictで返す
    def as_dict(self) -> list[dict[str, str]]:
        return [{"code": d.code, "area": d.area} for d in self.data]

    # JSONで返す
    def as_json(self) -> str:
        return json.dumps(self.as_dict(), ensure_ascii=False)
