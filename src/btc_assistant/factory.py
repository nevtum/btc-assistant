import logging
from os import environ

from analysis import BTCAssistant
from infrastructure.dynamodb import DynamoDB
from infrastructure.network import BTCPriceChecker
from infrastructure.storage import InMemoryStorage

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ENVIRONMENT = environ.get("ENVIRONMENT", "local")


def create_price_checker():
    return BTCPriceChecker()


# not used in production code. May affect performance
_in_memory_storage = InMemoryStorage()


def create_storage():
    logger.info("Environment variable ENVIRONMENT is set to {}!".format(ENVIRONMENT))
    if ENVIRONMENT == "prod":
        logger.warning("Production database DynamoDB is instantiated!")
        return DynamoDB("crypto-market-data-prod")
    elif ENVIRONMENT == "staging":
        logger.warning("Staging database DynamoDB is instantiated!")
        return DynamoDB("crypto-market-data-staging")
    elif ENVIRONMENT == "local":
        logger.info("Set ENVIRONMENT environment variable to PROD to use DynamoDB!")
        return _in_memory_storage
    else:
        raise EnvironmentError("Unknown environment set!")


def create_btc_assistant():
    class ConsolePresenter:
        def display(self, text):
            logger.info(text)

    return BTCAssistant(create_storage(), ConsolePresenter())
