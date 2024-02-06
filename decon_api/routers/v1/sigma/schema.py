
from pydantic import BaseModel, field_validator
from enum import Enum
from sigma.backends.microsoft365defender import Microsoft365DefenderBackend
from sigma.rule import SigmaRule
from sigma.validation import SigmaValidator
from sigma.validators.core import validators


class TargetPlatform(Enum):
    m365d = Microsoft365DefenderBackend


class Sigma(BaseModel):
    content: str
    target: Enum("SigmaTargets", [(t.name, t.name) for t in TargetPlatform])

    @field_validator('content')
    def valid_content(cls, v: str):
        try:
            sigma_content = SigmaRule.from_yaml(v)
            validator = SigmaValidator(validators.values())
            validator.validate_rule(sigma_content)
            return sigma_content
        except Exception as exc:
            raise ValueError(str(exc))

