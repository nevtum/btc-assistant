import logging
from os import environ

from pythonjsonlogger import jsonlogger

LOGLEVEL = environ.get("LOGLEVEL", "INFO")


def configure_root_logger_level():
    logger = logging.getLogger()
    logger.setLevel(LOGLEVEL)

    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter("%(asctime)s %(name)s %(levelname)s %(message)s")
    # formatter = jsonlogger.JsonFormatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logging.basicConfig(level=LOGLEVEL)
    logging.info(f"Logger level is set to: {LOGLEVEL}")

    logging.getLogger("botocore.vendored").setLevel(logging.WARNING)
    # add any extra namespaces to override the default configuration


def get_logger(namespace):
    logger = logging.getLogger(namespace)
    logger.setLevel(LOGLEVEL)
    return logger
