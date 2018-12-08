from os import environ

import factory
from log import get_logger

logger = get_logger(__name__)

def lambda_handler(event, context):
    logger.debug("Event payload: {}".format(event))
    logger.debug("Context: {}".format(context))
    
    checker = factory.create_price_checker()
    storage = factory.create_storage()
    data = checker.get_btc_day_market_data('AUD')
    storage.store_record(data)
    return "Success"

if __name__ == '__main__':
    lambda_handler(None, None)
