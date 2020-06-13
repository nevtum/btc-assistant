import logging

import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class WriteRecordToDynamoDBCommand:
    def __init__(self, table_name):
        self.client = boto3.client("dynamodb")
        self.table_name = table_name

    def __call__(self, data):
        logger.debug("Attempting to save data to dynamodb table '{}'".format(self.table_name))
        kwargs = self._build_put_kwargs(data)
        resp = self.client.put_item(ReturnConsumedCapacity="TOTAL", **kwargs)
        logger.info("Consumed capacity: {}".format(resp["ConsumedCapacity"]))
        return resp

    def _build_put_kwargs(self, data):
        assert data.price >= 0
        assert data.volume >= 0
        return {
            "TableName": self.table_name,
            "Item": {
                "ticker_symbol": {"S": data.symbol},
                "unix_timestamp_utc": {"N": str(data.timestamp.timestamp())},
                "price": {"S": str(data.price)},
                "volume": {"S": str(data.volume)},
                "url": {"S": data.url},
            },
        }
