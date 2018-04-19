
import logging
from os import environ

import boto3
from btc_assistant.btc_utils import BTCPriceChecker

LOGLEVEL = environ.get("LOGLEVEL", "INFO")

logging.basicConfig(level=LOGLEVEL)
logging.getLogger('botocore.vendored').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(LOGLEVEL)


def save_to_db(data):
    client = boto3.client("dynamodb")
    logger.debug("Attempting to save data to dynamodb table crypto-market-data")
    resp = client.put_item(
        TableName='crypto-market-data',
        Item={
            'utc_timestamp': { 'S': data.timestamp.isoformat() },
            'currency_code': { 'S': 'BTC' },
            'price': { 'S':  str(data.last_price) },
            'volume': { 'S': str(data.volume) },
            'url': { 'S': 'www.independentreserve.com'}
        },
        ReturnConsumedCapacity='TOTAL'
    )
    logger.info("Consumed capacity: {}".format(resp["ConsumedCapacity"]))

def handler(event, context):
    price_checker = BTCPriceChecker()
    logger.debug("Getting BTC market data from Independent Reserve...")
    data = price_checker.get_btc_day_market_data("AUD")
    logger.info("Data retrieved: {}".format(data.raw_data))
    save_to_db(data)
    return "Success"

if __name__ == '__main__':
    handler(None, None)
