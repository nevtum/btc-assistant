import uvicorn
from fastapi import FastAPI

from presentation import configure_api, configure_app


def create_app():
    app = FastAPI(debug=True)
    # app.config.from_object(FlaskConfig)

    configure_app(app)
    configure_api(app)
    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("__main__:app", port=5000, reload=True)
