import logging

import boto3
from .storage import StorageBase

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class DynamoDB(StorageBase):
    def store_record(self, data):
        client = boto3.client("dynamodb")
        logger.debug("Attempting to save data to dynamodb table crypto-market-data")
        resp = client.put_item(
            TableName='crypto-market-data',
            Item={
                'utc_timestamp': { 'S': data.timestamp.isoformat() },
                'currency_code': { 'S': 'BTC' },
                'price': { 'S':  str(data.last_price) },
                'volume': { 'S': str(data.volume) },
                'url': { 'S': 'www.independentreserve.com'}
            },
            ReturnConsumedCapacity='TOTAL'
        )
        logger.info("Consumed capacity: {}".format(resp["ConsumedCapacity"]))
