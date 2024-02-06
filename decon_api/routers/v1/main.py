from fastapi import APIRouter, Depends, Security
from routers.v1.sigma import api as SigmaAPI

api_v1 = APIRouter()

api_v1.include_router(SigmaAPI.router,
    tags=['sigma']
)
