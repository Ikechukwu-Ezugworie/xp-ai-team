from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_messages():
    pass  # TODO: implement


@router.post("/")
async def send_message():
    pass  # TODO: implement
