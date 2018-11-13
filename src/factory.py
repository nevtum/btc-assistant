import logging
from os import environ

from btc_assistant.aws_storage import DynamoDB
from btc_assistant.btc_utils import BTCPriceChecker
from btc_assistant.storage import InMemoryStorage
from btc_assistant.app import BTCAssistant

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ENVIRONMENT = environ.get("ENVIRONMENT", "TEST")

def create_price_checker():
    return BTCPriceChecker()

# not used in production code. May affect performance
_in_memory_storage = InMemoryStorage()

def create_storage():
    logger.info("Environment variable ENVIRONMENT is set to {}!".format(ENVIRONMENT))
    if ENVIRONMENT == "PROD":
        logger.warning("Production database DynamoDB is instantiated!")
        return DynamoDB('crypto-market-data')
    elif ENVIRONMENT == "STAGING":
        logger.warning("Staging database DynamoDB is instantiated!")
        return DynamoDB('crypto-market-data-staging')
    elif ENVIRONMENT == "TEST":
        logger.info("Set ENVIRONMENT environment variable to PROD to use DynamoDB!")
        return _in_memory_storage
    else:
        raise EnvironmentError("Unknown environment set!")

def create_btc_assistant():
    class ConsolePresenter:
        def display(self, text):
            logger.info(text)
    
    return BTCAssistant(create_storage(), ConsolePresenter())
