from fastapi import APIRouter, status

router = APIRouter()

@router.get("/ping")
async def pong():
    return {"status":"pong", "status_code":status.HTTP_200_OK}