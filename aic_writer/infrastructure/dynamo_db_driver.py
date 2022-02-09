"""
データをDynamoDBに格納する
"""
import boto3

from aic_writer.adapter.interface import DBDriver


class DynamoDBDriver(DBDriver):
    def __init__(self, endpoint, table_name: str = "AreaInformationCity"):
        if endpoint:
            self.dynamodb = boto3.resource("dynamodb", endpoint_url=endpoint)
        else:
            self.dynamodb = boto3.resource("dynamodb", region_name="us-west-2")

        self.table_name = table_name
        self.client = boto3.client("dynamodb")

    def delete_table(self):
        """
        テーブルを削除する(存在する場合のみ)
        """
        existing_tables = self.client.list_tables()["TableNames"]

        # 存在する場合は削除し、削除完了まで待つ
        if self.table_name in existing_tables:
            table = self.dynamodb.Table(self.table_name)
            table.delete()
            waiter = self.client.get_waiter("table_not_exists")
            waiter.wait(TableName=self.table_name, WaiterConfig={"Delay": 5})

    def create_table(self):
        """
        テーブルを作成する
        """
        # 本当は設定データは外で管理したいところ...
        self.dynamodb.create_table(
            TableName=self.table_name,
            KeySchema=[
                {"AttributeName": "code", "KeyType": "HASH"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "code", "AttributeType": "S"},
            ],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )

        # 作成完了まで待つ
        waiter = self.client.get_waiter("table_exists")
        waiter.wait(TableName=self.table_name, WaiterConfig={"Delay": 5})

    def create_data(self, data: list[dict[str, str]]):
        """
        受け取ったデータをDynamoDBに入れる
        """
        table = self.dynamodb.Table(self.table_name)

        # データの数が多いのでバッチ処理する
        with table.batch_writer() as batch:
            for datum in data:
                batch.put_item(Item=datum)
