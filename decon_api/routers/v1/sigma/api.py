from fastapi import APIRouter
from routers.v1.sigma.schema import Sigma, TargetPlatform


router = APIRouter()

@router.post('/sigma/convert')
async def convert_sigma(data: Sigma) -> dict:
    selected_backend = TargetPlatform[data.target.value].value()
    return {'output': selected_backend.convert_rule(data.content)[0]}
