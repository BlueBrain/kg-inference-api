from typing import List
from pydantic import BaseModel


class InputParameter(BaseModel):
    """An input parameter of a rule"""
    name: str
    payload: dict


class Rule(BaseModel):
    """A data generalization rule"""
    name: str
    description: str
    targetResourceType: str
    inputParameters: List[InputParameter]
