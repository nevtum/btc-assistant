from . import log
from .common import *

APP_ENVIRONMENT = "local" # TODO: change to environment variable

if APP_ENVIRONMENT == "local":
    from .local import *
else:
    raise EnvironmentError(f"No config for '{APP_ENVIRONMENT}' environment implemented!")
