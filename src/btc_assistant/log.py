import logging
from os import environ

LOGLEVEL = environ.get("LOGLEVEL", "INFO")

def _set_root_logger_level():
    logging.info("Logger level is set to: {}".format(logging.INFO))
    logging.basicConfig(
        level=LOGLEVEL,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logging.getLogger().setLevel(LOGLEVEL)
    logging.getLogger('botocore.vendored').setLevel(logging.WARNING)
    # add any extra namespaces to override the default configuration

def get_logger(namespace):
    logger = logging.getLogger(namespace)
    logger.setLevel(LOGLEVEL)
    return logger

_set_root_logger_level()