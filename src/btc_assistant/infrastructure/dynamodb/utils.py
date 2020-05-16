from log import get_logger

from .builders import CryptoDynamoQueryBuilder, CryptoDynamoWriteRecordBuilder
from .core import DynamoQueryPaginator, execute_insert

logger = get_logger(__name__)


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
        return DynamoQueryPaginator(builder.build_query_kwargs())
