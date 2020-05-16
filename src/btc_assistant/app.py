import logging
from os import environ

from infrastructure.dynamodb import DynamoDB
from infrastructure.network import BTCPriceChecker

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ENVIRONMENT = environ.get("ENV", "local")


def create_storage():
    logger.info(f"Environment variable ENVIRONMENT is set to {ENVIRONMENT}!")
    if ENVIRONMENT in ("prod", "staging", "test", "local"):
        return DynamoDB(f"crypto-market-data-{ENVIRONMENT}")
    else:
        raise EnvironmentError("Unknown environment set!")


class WorkerApp:
    def __init__(self):
        self.checker = BTCPriceChecker()
        self.storage = create_storage()

    def create_handler(self):
        def func(event, context):
            logger.debug("Event payload: {}".format(event))
            logger.debug("Context: {}".format(context))

            data = self.checker.get_btc_day_market_data("USD")
            self.storage.store_record(data)

            return "SUCCESS"

        return func
