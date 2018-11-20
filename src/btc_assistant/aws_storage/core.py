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

class DynamoQueryPaginator:
    def __init__(self, query_kwargs):
        self.query_kwargs = query_kwargs
        self.no_more_records = False
        self.buffer = deque()

    def _fetch_next_records(self):
        resp = execute_query(**self.query_kwargs)
        
        if 'LastEvaluatedKey' in resp:
            logger.debug("There is more data to retrieve!")
            self.query_kwargs['ExclusiveStartKey'] = resp['LastEvaluatedKey']
        else:
            if 'ExclusiveStartKey' in self.query_kwargs:
                self.query_kwargs.pop('ExclusiveStartKey')
            self.no_more_records = True
        
        return resp.get('Items', [])
    
    def __iter__(self):
        return self

    def __next__(self):
        if len(self.buffer) > 0:
            return self.buffer.popleft()

        if self.no_more_records:
            raise StopIteration("No more records!")

        self.buffer = deque(self._fetch_next_records())