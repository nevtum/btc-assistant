from . import router


@router.get("/test")
async def index():
    return "Hi!"
