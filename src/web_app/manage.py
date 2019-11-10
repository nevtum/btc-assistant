import uvicorn
from fastapi import FastAPI

from config import DEBUG
from presentation import configure_api, configure_app


def create_app():
    app = FastAPI(debug=DEBUG)

    configure_app(app)
    configure_api(app)
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, port=5000)
    # uvicorn.run("__main__:app", port=5000, reload=True)
