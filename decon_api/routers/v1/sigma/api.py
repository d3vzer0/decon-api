from fastapi import APIRouter, HTTPException
from decon_api.routers.v1.sigma.schema import Sigma, TargetPlatform

router = APIRouter()


@router.get('/sigma/targets')
async def sigma_targets() -> list:
    return [(t.name) for t in TargetPlatform]


@router.post('/sigma/convert')
async def convert_sigma(data: Sigma) -> dict:
    selected_backend = TargetPlatform[data.target.value].value()
    try:
        converted_rule = selected_backend.convert_rule(data.content)[0]
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))
    return {'output': converted_rule}
