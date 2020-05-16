from app import WorkerApp
from log import configure_root_logger_level

configure_root_logger_level()
app = WorkerApp()

lambda_handler = app.create_handler()

if __name__ == "__main__":
    lambda_handler(None, None)
