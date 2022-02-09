from abc import ABC, abstractmethod


class IClient(ABC):
    @abstractmethod
    def get_as_str(self, url: str) -> str:
        ...

    @abstractmethod
    def get_as_bin(self, url: str) -> bytes:
        ...


class IExcelReader(ABC):
    @staticmethod
    @abstractmethod
    def get_data(excel_data: bytes) -> list[list[str]]:
        ...


class DBDriver(ABC):
    @abstractmethod
    def delete_table(self):
        ...

    @abstractmethod
    def create_table(self):
        ...

    @abstractmethod
    def create_data(self, data: list[dict[str, str]]):
        ...
