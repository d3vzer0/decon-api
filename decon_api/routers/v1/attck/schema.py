
from pydantic import BaseModel, field_validator
from enum import Enum


class Technique(BaseModel):
    id: str
    technique_id: str
    name: str
    description: str
    platforms: list[str]
    permissions_required: list[str]
    data_sources: list[str]
    references: list
    is_subtechnique: bool
    kill_chain_phases: list[str]


class Actor(BaseModel):
    id: str
    actor_id: str
    name: str
    references: list
    aliases: list[str]
    description: str
