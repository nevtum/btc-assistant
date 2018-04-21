import logging
from os import environ

from btc_assistant.aws_storage import DynamoDB
from btc_assistant.btc_utils import BTCPriceChecker
from btc_assistant.storage import FakeStorage

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

PRODUCTION_DB = environ.get("PRODUCTION_DB", False)

def create_price_checker():
    return BTCPriceChecker()

def create_storage():
    logger.info("Environment variable PRODUCTION_DB is set to {}!".format(PRODUCTION_DB))        
    if PRODUCTION_DB:
        logger.warning("Production database DynamoDB is instantiated!")        
        return DynamoDB()
    else:
        logger.info("Set PRODUCTION_DB environment variable to True to use DynamoDB!")
        return FakeStorage()
