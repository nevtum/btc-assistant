import boto3

from .log import get_logger
from .storage import StorageBase

logger = get_logger(__name__)

class CryptoQuery:
    def __init__(self, table_name):
        self.table_name = table_name
        self.item_limit = 500
        self.last_eval_key = None
        self.start_datetime = None
        self.end_datetime = None

    def since(self, start_datetime):
        self.start_datetime = start_datetime
        return self

    def until(self, end_datetime):
        self.end_datetime = end_datetime
        return self

    def with_crypto_code(self, currency_code):
        self.currency_code = currency_code
        return self

    def with_last_key_evaluated(self, a_dict):
        self.last_eval_key = a_dict
        return self

    def build_query_args(self):
        args = {
            'TableName': self.table_name,
            'IndexName': 'crypto-timestamp-index',
            'Limit': self.item_limit,
            'ReturnConsumedCapacity': 'INDEXES',
            'KeyConditionExpression': self._build_key_condition_expression(),
            'ExpressionAttributeValues': self._build_expression_attributes(),
        }
        if self.last_eval_key:
            args['ExclusiveStartKey'] = self.last_eval_key
        return args

    def _build_key_condition_expression(self):
        base_query = 'currency_code = :sym'
        if self.start_datetime and self.end_datetime:
            return '{} AND utc_timestamp BETWEEN :t1 AND :t2'.format(base_query)
        return base_query

    def _build_expression_attributes(self):
        return {
            ':sym': {
                'S': self.currency_code,
            }
        }

class DynamoDB(StorageBase):
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
    
    def execute_query(self, query_obj):
        resp = self.client.query(**query_obj.build_query_args())
        logger.info("Consumed capacity: {}".format(resp["ConsumedCapacity"]))
        return resp

    def enumerate_records(self, currency_code, start_datetime=None, end_datetime=None):
        query_obj = CryptoQuery(self.table_name).with_crypto_code('BTC')
        resp = self.execute_query(query_obj)
        for item in resp.get('Items', []):
            yield item
        while 'LastEvaluatedKey' in resp:
            logger.debug("There is more data to retrieve!")
            query_obj.with_last_key_evaluated(resp['LastEvaluatedKey'])
            resp = self.execute_query(query_obj)
            for item in resp.get('Items', []):
                yield item