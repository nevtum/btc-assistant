import logging
from os import environ

from btc_assistant.aws_storage import DynamoDB
from btc_assistant.btc_utils import BTCPriceChecker
from btc_assistant.storage import FakeStorage

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ENVIRONMENT = environ.get("ENVIRONMENT", "TEST")

def create_price_checker():
    return BTCPriceChecker()

def create_storage():
    logger.info("Environment variable ENVIRONMENT is set to {}!".format(ENVIRONMENT))        
    if ENVIRONMENT == "PROD":
        logger.warning("Production database DynamoDB is instantiated!")        
        return DynamoDB()
    elif ENVIRONMENT == "TEST":
        logger.info("Set ENVIRONMENT environment variable to PROD to use DynamoDB!")
        return FakeStorage()
    else:
        raise EnvironmentError("Unknown environment set!")
