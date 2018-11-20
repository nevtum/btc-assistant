from datetime import datetime

import boto3

from ..log import get_logger
from .queries import CryptoQueryBuilder, DynamoItemsIterator

logger = get_logger(__name__)

class CryptoDynamoWriteRecordBuilder:
    def __init__(self, table_name):
        self.table_name = table_name
    
    def at_timestamp(self, timestamp):
        self.timestamp = timestamp
        return self
    
    def price(self, value):
        self.price = value
        return self
    
    def volume(self, value):
        self.volume = value
        return self
    
    def from_source(self, url):
        self.url = url
        return self

    def build_put_kwargs(self):
        assert(isinstance(self.timestamp, datetime))
        assert(self.price >= 0)
        assert(self.volume >= 0)
        return {
            'TableName': self.table_name,
            'Item': {
                'utc_timestamp': { 'S': self.timestamp.isoformat() },
                'currency_code': { 'S': 'BTC' },
                'price': { 'S':  str(self.price) },
                'volume': { 'S': str(self.volume) },
                'url': { 'S': self.url }
            }
        }

class DynamoDB:
    def __init__(self, table_name):
        self.table_name = table_name
        self.client = boto3.client("dynamodb")

    def store_record(self, data):
        logger.debug("Attempting to save data to dynamodb table '{}'".format(self.table_name))
        kwargs = (
            CryptoDynamoWriteRecordBuilder(self.table_name)
            .at_timestamp(data.timestamp)
            .price(data.last_price)
            .volume(data.volume)
            .from_source(data.url)
            .build_put_kwargs()
        )
        resp = self.client.put_item(ReturnConsumedCapacity='TOTAL', **kwargs)
        logger.info("Consumed capacity: {}".format(resp["ConsumedCapacity"]))

    def enumerate_records(self, currency_code, start_datetime=None, end_datetime=None):
        builder = (
            CryptoQueryBuilder(self.table_name)
            .with_crypto_code(currency_code)
            .since(start_datetime)
            .until(end_datetime)
        )
        return DynamoItemsIterator(builder)