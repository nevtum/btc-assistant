from starlette.config import Config

from . import log
from .common import *

config = Config()

APP_ENVIRONMENT = config("APP_ENV", default="local")

if APP_ENVIRONMENT == "local":
    from .local import *
elif APP_ENVIRONMENT == "production":
    from .prod import *
else:
    raise EnvironmentError(f"No config for '{APP_ENVIRONMENT}' environment implemented!")
