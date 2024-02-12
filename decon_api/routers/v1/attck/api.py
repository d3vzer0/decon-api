from fastapi import APIRouter, HTTPException
from decon_api.routers.v1.attck.intel import MitreAttck
from decon_api.routers.v1.attck.schema import Technique, Actor


router = APIRouter()

attck = MitreAttck.from_cti()

@router.get('/attck/actor/{actor_id}')
async def get_actor(actor_id: str) -> Actor:
    get_actor = attck.actors.get(actor_id, None)
    if not get_actor:
        raise HTTPException(status_code=404, detail="Actor not found")
    return get_actor.actor


@router.get('/attck/technique/{technique_id}')
async def get_technique(technique_id: str) -> Technique:
    get_technique = attck.techniques.get(technique_id, None)
    if not get_technique:
        raise HTTPException(status_code=404, detail="Technique not found")
    return get_technique.technique