import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# configure custom levels for 3rd party libs or other modules
logging.getLogger("botocore").setLevel(logging.WARNING)