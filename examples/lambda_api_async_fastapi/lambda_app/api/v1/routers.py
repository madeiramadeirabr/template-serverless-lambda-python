from fastapi import APIRouter
from .ping import ping

router = APIRouter()

router.include_router(ping.router)
