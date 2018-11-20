from collections import deque

from ..log import get_logger
from .builders import CryptoDynamoQueryBuilder, CryptoDynamoWriteRecordBuilder
from .core import execute_insert, execute_query

logger = get_logger(__name__)

class DynamoItemsIterator:
    def __init__(self, query_builder):
        self.query_builder = query_builder
        self.no_more_records = False
        self.buffer = deque()

    def _fetch_next_records(self):
        resp = execute_query(**self.query_builder.build_query_kwargs())
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

class DynamoDB:
    def __init__(self, table_name):
        self.table_name = table_name

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
        resp = execute_insert(**kwargs)
        return resp

    def enumerate_records(self, currency_code, start_datetime=None, end_datetime=None):
        builder = (
            CryptoDynamoQueryBuilder(self.table_name)
            .with_crypto_code(currency_code)
            .since(start_datetime)
            .until(end_datetime)
        )
        return DynamoItemsIterator(builder)
