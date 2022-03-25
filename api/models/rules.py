from typing import List, Optional
from fastapi_camelcase import CamelModel
from pydantic import BaseModel


class InputParameter(BaseModel):
    """An input parameter of a rule"""
    name: str
    payload: dict


class RuleOutput(CamelModel):
    """A data generalization rule output"""
    id: str
    name: str
    description: str
    resource_type: str
    input_parameters: List[InputParameter]


class RuleInput(BaseModel):
    """A data generalization rule input"""
    id: str


class RulesBody(CamelModel):
    """Request body for rules"""
    resource_types: Optional[List[str]] = None
    input_filters: Optional[List] = None
