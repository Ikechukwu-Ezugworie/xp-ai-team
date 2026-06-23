from fastapi import APIRouter
router = APIRouter()

@router.get("/")
async def get_rooms():
    pass  # TODO: implement

@router.post("/")
async def create_room():
    pass  # TODO: implement
