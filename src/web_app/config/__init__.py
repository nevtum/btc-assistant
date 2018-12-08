APP_ENVIRONMENT = "local"

if APP_ENVIRONMENT == "local":
    from .local import *
else:
    raise EnvironmentError(f"No config for '{APP_ENVIRONMENT}' environment implemented!")