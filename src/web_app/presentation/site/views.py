from . import router


@router.get("/")
async def index():
    return "Hi!"
