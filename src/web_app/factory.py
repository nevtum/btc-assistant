from config import CRYPTO_TIMESERIES_INDEX_NAME, DYNAMODB_TABLE_NAME
from infrastructure.dynamodb import CryptoMarketDataGateway


def create_market_data_gateway():
    return CryptoMarketDataGateway(DYNAMODB_TABLE_NAME, CRYPTO_TIMESERIES_INDEX_NAME)