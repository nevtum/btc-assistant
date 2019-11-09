from fastapi import APIRouter

router = APIRouter()

from . import views


def configure_app(app):
    app.include_router(router)
