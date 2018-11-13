import boto3

from ..log import get_logger
from .queries import CryptoQueryBuilder, DynamoItemsIterator

logger = get_logger(__name__)

class DynamoDB:
    def __init__(self, table_name):
        self.table_name = table_name
        self.client = boto3.client("dynamodb")

    def store_record(self, data):
        logger.debug("Attempting to save data to dynamodb table crypto-market-data")
        resp = self.client.put_item(
            TableName=self.table_name,
            Item={
                'utc_timestamp': { 'S': data.timestamp.isoformat() },
                'currency_code': { 'S': 'BTC' },
                'price': { 'S':  str(data.last_price) },
                'volume': { 'S': str(data.volume) },
                'url': { 'S': data.url }
            },
            ReturnConsumedCapacity='TOTAL'
        )
        logger.info("Consumed capacity: {}".format(resp["ConsumedCapacity"]))

    def enumerate_records(self, currency_code, start_datetime=None, end_datetime=None):
        builder = CryptoQueryBuilder(self.table_name).with_crypto_code('BTC')
        return DynamoItemsIterator(builder)