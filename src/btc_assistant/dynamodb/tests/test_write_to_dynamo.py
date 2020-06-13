import unittest
from datetime import datetime

from ..write import WriteRecordToDynamoDBCommand


class DataObj:
    pass


class TestDynamoWriteCommands(unittest.TestCase):
    def test_write_data_to_dynamo_args(self):
        cmd = WriteRecordToDynamoDBCommand(table_name="my-dynamo-table")

        data = DataObj()
        data.price = 12412
        data.volume = 513
        data.symbol = "BTCUSD"
        data.timestamp = datetime.now()
        data.url = "http://an.exchange.com/price"

        actual = cmd._build_put_kwargs(data)

        expected = {
            "TableName": "my-dynamo-table",
            "Item": {
                "ticker_symbol": {"S": "BTCUSD"},
                "unix_timestamp_utc": {"N": str(data.timestamp.timestamp())},
                "price": {"S": "12412"},
                "volume": {"S": "513"},
                "url": {"S": "http://an.exchange.com/price"},
            },
        }

        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
