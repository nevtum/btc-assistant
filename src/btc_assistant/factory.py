import logging
from os import environ

from infrastructure.dynamodb import DynamoDB
from infrastructure.network import BTCPriceChecker

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ENVIRONMENT = environ.get("ENV", "local")


def create_price_checker():
    return BTCPriceChecker()


def create_storage():
    logger.info(f"Environment variable ENVIRONMENT is set to {ENVIRONMENT}!")
    if ENVIRONMENT == "prod":
        logger.warning("Production database DynamoDB is instantiated!")
        return DynamoDB("crypto-market-data-prod")
    elif ENVIRONMENT == "staging":
        logger.warning("Staging database DynamoDB is instantiated!")
        return DynamoDB("crypto-market-data-staging")
    else:
        raise EnvironmentError("Unknown environment set!")
