from fastapi import APIRouter

router = APIRouter()

from . import views


def configure_api(app):
    app.include_router(router, prefix="/api")
