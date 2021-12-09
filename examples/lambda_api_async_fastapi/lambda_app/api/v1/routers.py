from fastapi import APIRouter
from .ping import ping
from .subsidiaries import subsidiaries

router = APIRouter()

router.include_router(ping.router)
router.include_router(subsidiaries.router)
