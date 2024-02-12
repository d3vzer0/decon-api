from fastapi import APIRouter, Depends, Security
from decon_api.routers.v1.sigma import api as SigmaAPI
from decon_api.routers.v1.attck import api as AttckAPI


api_v1 = APIRouter()

api_v1.include_router(SigmaAPI.router,
    tags=['sigma']
)

api_v1.include_router(AttckAPI.router,
    tags=['attck']
)
