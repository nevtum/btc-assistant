from log import get_logger

from .builders import CryptoDynamoQueryBuilder
from .core import DynamoQueryPaginator, execute_insert

logger = get_logger(__name__)


class DynamoDB:
    def __init__(self, table_name):
        self.table_name = table_name

    def store_record(self, data):
        logger.debug("Attempting to save data to dynamodb table '{}'".format(self.table_name))
        kwargs = self._build_put_kwargs(data)
        resp = execute_insert(**kwargs)
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

    def enumerate_records(self, currency_code, start_datetime=None, end_datetime=None):
        builder = (
            CryptoDynamoQueryBuilder(self.table_name)
            .with_crypto_code(currency_code)
            .since(start_datetime)
            .until(end_datetime)
        )
        return DynamoQueryPaginator(builder.build_query_kwargs())
