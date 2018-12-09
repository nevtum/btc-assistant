from .builders import CryptoDynamoExpressionBuilder, QueryBuilder
from config import CRYPTO_TIMESERIES_INDEX_NAME, DYNAMODB_TABLE_NAME
from .core import execute_query

class CryptoMarketDataGateway:
    def __init__(self, table_name, index_name):
        self.table_name = table_name
        self.index_name = index_name

    def get_bitcoin_market_data(self, since_datetime, limit=65):
        kwargs = (
            QueryBuilder(self.table_name, self.index_name)
            .set_batch_size_to(limit)
            .with_query_expression(
                CryptoDynamoExpressionBuilder()
                .with_crypto_code("BTC")
                .since(since_datetime)
            )
            .build_query_kwargs()
        )
        resp = execute_query(**kwargs)
        return resp