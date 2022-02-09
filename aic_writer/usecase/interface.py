from abc import ABC, abstractmethod

from aic_writer.domain import AreaInformationCityList


class ReadRepository(ABC):
    @abstractmethod
    def get_tec_material_page(self) -> str:
        ...

    @abstractmethod
    def get_code_list(self, target: str) -> AreaInformationCityList:
        ...


class WriteRepository(ABC):
    @abstractmethod
    def update(self, data: list[dict[str, str]]):
        ...


class IParser(ABC):
    @abstractmethod
    def parse(self, html: str) -> str:
        ...
