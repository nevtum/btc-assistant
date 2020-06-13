import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class SaveRecordToMemoryCommand:
    def __init__(self, records=[]):
        self.records = records

    def __call__(self, record):
        logger.info("Storing data", extra={"payload": record})
        self.records.append(record)
