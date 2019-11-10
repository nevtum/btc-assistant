from starlette.config import Config

config = Config()

DYNAMODB_TABLE_NAME = config("DYNAMODB_TABLE_NAME", default="crypto-market-data")
CRYPTO_TIMESERIES_INDEX_NAME = config(
    "CRYPTO_TIMESERIES_INDEX_NAME", default="crypto-timestamp-index"
)

