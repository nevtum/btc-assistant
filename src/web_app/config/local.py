from starlette.config import Config

config = Config()

DEBUG = config("DEBUG", default=True)
