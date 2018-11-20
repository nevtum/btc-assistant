from collections import deque

import boto3

from ..log import get_logger

logger = get_logger(__name__)

_client = boto3.client("dynamodb")

def execute_query(query_builder):
    kwargs = query_builder.build_query_kwargs()
    logger.info(kwargs)
    resp = _client.query(**kwargs)
    logger.info("Consumed capacity: {}".format(resp["ConsumedCapacity"]))
    return resp

class CryptoQueryBuilder:
    def __init__(self, table_name):
        self.table_name = table_name
        self.item_limit = 500
        self.last_eval_key = None
        self.start_datetime = None
        self.end_datetime = None
    
    def set_batch_size_to(self, batch_size):
        self.item_limit = batch_size
        return self

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

    def build_query_kwargs(self):
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
            return f'{base_query} AND utc_timestamp BETWEEN :t1 AND :t2'
        elif self.start_datetime and not self.end_datetime:
            return f'{base_query} AND utc_timestamp >= :t1'
        elif not self.start_datetime and self.end_datetime:
            return f'{base_query} AND utc_timestamp <= :t2'
        return base_query

    def _build_expression_attributes(self):
        query_exp = {
            ':sym': {
                'S': self.currency_code,
            }
        }
        if self.start_datetime:
            query_exp[':t1'] = { 'S': self.start_datetime.isoformat() }
        if self.end_datetime:
            query_exp[':t2'] = { 'S': self.end_datetime.isoformat() }
        return query_exp

class DynamoItemsIterator:
    def __init__(self, query_builder):
        self.query_builder = query_builder
        self.no_more_records = False
        self.buffer = deque()

    def _fetch_next_records(self):
        resp = execute_query(self.query_builder)
        if 'LastEvaluatedKey' in resp:
            logger.debug("There is more data to retrieve!")
            self.query_builder.with_last_key_evaluated(resp['LastEvaluatedKey'])
        else:
            self.no_more_records = True
        return resp.get('Items', [])
    
    def __iter__(self):
        return self

    def __next__(self):
        if len(self.buffer) > 0:
            return self.buffer.popleft()

        if self.no_more_records:
            raise StopIteration("No more records!")

        self.buffer = deque(self._fetch_next_records())
