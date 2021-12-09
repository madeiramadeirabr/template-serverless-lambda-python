from fastapi import APIRouter, status
from fastapi.security import OAuth2PasswordBearer
from .models import User
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

@router.get("/token")
async def get_token():
    return {"status":"pong", "status_code":status.HTTP_200_OK}