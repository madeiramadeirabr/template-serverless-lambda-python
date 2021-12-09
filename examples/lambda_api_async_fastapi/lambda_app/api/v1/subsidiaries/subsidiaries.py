from fastapi import APIRouter, status, Depends
from lambda_app.auth.authenticate import oauth2_scheme

router = APIRouter()

@router.get("/subsidiaries")
async def subsidiaries(token:str = Depends(oauth2_scheme)):
    return {"status":"subsidiaries", "status_code":status.HTTP_200_OK}