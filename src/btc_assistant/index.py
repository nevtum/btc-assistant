from os import environ

from app import AppFactory
from log import configure_root_logger_level

configure_root_logger_level()

ENVIRONMENT = environ.get("ENV", "local")
lambda_handler = AppFactory(ENVIRONMENT).create_handler()

if __name__ == "__main__":
    lambda_handler({}, None)
