import boto3

from log import get_logger

logger = get_logger(__name__)


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
