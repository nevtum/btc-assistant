from app import WorkerApp

app = WorkerApp()

lambda_handler = app.create_handler()

if __name__ == "__main__":
    lambda_handler(None, None)
