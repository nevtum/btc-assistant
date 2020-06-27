import logging
from os import environ

from pythonjsonlogger import jsonlogger

LOGLEVEL = environ.get("LOGLEVEL", "INFO")


def configure_root_logger_level():
    logger = logging.getLogger()

    for h in logger.handlers:
        logger.removeHandler(h)

    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter("%(asctime)s %(name)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(LOGLEVEL)
    logging.info(f"Logger level is set", extra={"log_level": LOGLEVEL})

    logging.getLogger("botocore.vendored").setLevel(logging.WARNING)
    # add any extra namespaces to override the default configuration


def get_logger(namespace):
    logger = logging.getLogger(namespace)
    logger.setLevel(LOGLEVEL)
    return logger
