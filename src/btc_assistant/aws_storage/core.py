import boto3

from ..log import get_logger

logger = get_logger(__name__)

_client = boto3.client("dynamodb")

def execute_query(**kwargs):
    logger.info(kwargs)
    resp = _client.query(**kwargs)
    logger.info("Consumed capacity: {}".format(resp["ConsumedCapacity"]))
    return resp

def execute_insert(**kwargs):
    logger.info(kwargs)
    resp = _client.put_item(ReturnConsumedCapacity='TOTAL', **kwargs)
    logger.info("Consumed capacity: {}".format(resp["ConsumedCapacity"]))
    return resp