from aic_writer.adapter import DBRepository, JMARepository, TecMaterialParser
from aic_writer.infrastructure import AreaInformationCityReader, DynamoDBDriver, HTTPClient
from aic_writer.usecase.interactor import AICInteractor


def update_db():

    client = HTTPClient()
    # Local
    # driver = DynamoDBDriver(endpoint="http://localhost:8000", table_name="AreaInformationCity")
    driver = DynamoDBDriver(endpoint="", table_name="AreaInformationCity")
    reader = AreaInformationCityReader()
    parser = TecMaterialParser()
    read_repository = JMARepository(client=client, reader=reader)
    write_repository = DBRepository(driver=driver)
    interactor = AICInteractor(
        read_repository=read_repository, write_repository=write_repository, parser=parser
    )

    interactor.handle()
