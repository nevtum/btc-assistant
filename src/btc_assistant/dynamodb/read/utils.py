from .builders import CryptoDynamoQueryBuilder
from .core import DynamoQueryPaginator


class DynamoDBReader:
    def __init__(self, table_name):
        self.table_name = table_name

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
