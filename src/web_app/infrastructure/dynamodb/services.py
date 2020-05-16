from datetime import datetime

from config import CRYPTO_TIMESERIES_INDEX_NAME, DYNAMODB_TABLE_NAME

from .builders import CryptoDynamoExpressionBuilder, QueryBuilder
from .core import execute_query
from dateutil import parser


class BitcoinPriceDTO:
    def __init__(self, a_dict):
        self.data = a_dict

    @property
    def utc_timestamp(self):
        datetime_str = self.data["utc_timestamp"]["S"]
        return parser.parse(datetime_str)

    @property
    def value(self):
        return float(self.data["price"]["S"])

    @property
    def volume(self):
        return float(self.data["volume"]["S"])

    def as_dict(self):
        return dict(utc_timestamp=self.utc_timestamp, value=self.value, volume=self.volume)


class CryptoMarketDataGateway:
    def __init__(self, table_name, index_name):
        self.table_name = table_name
        self.index_name = index_name

    def get_bitcoin_market_data(self, since_datetime, limit=65):
        kwargs = (
            QueryBuilder(self.table_name, self.index_name)
            .set_batch_size_to(limit)
            .with_query_expression(
                CryptoDynamoExpressionBuilder().with_crypto_code("BTC").since(since_datetime)
            )
            .build_query_kwargs()
        )
        resp = execute_query(**kwargs)
        dtos = map(lambda a_dict: BitcoinPriceDTO(a_dict), resp["Items"])
        return list(dtos)
