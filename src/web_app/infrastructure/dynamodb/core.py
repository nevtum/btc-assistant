import logging
from collections import deque

import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

_client = boto3.client("dynamodb")

def execute_query(**kwargs):
    logger.info(kwargs)
    resp = _client.query(**kwargs)
    logger.info("Consumed capacity: {}".format(resp["ConsumedCapacity"]))
    return resp
