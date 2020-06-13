import logging

from dynamodb import WriteRecordToDynamoDBCommand
from network import CheckBTCPriceData
from storage import SaveRecordToMemoryCommand

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class AppFactory:
    def __init__(self, env):
        self.env = env

    def create_handler(self) -> callable:
        """ Bootstraps and returns a lambda handler """

        get_btc_data = CheckBTCPriceData()
        store_record = self._bootstrap_save_record_command()

        def handler(event, context):
            logger.debug("Event payload: {}".format(event))
            logger.debug("Context: {}".format(context))

            data = get_btc_data("USD")
            store_record(data)

            return "SUCCESS"

        return handler

    def _bootstrap_save_record_command(self):
        logger.info(f"Environment variable ENVIRONMENT is set to {self.env}!")
        if self.env in ("prod", "staging", "test"):
            return WriteRecordToDynamoDBCommand(f"crypto-market-data-{self.env}")
        elif self.env in ("local"):
            return SaveRecordToMemoryCommand()
        else:
            raise EnvironmentError("Unknown environment set!")
