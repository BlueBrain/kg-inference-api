from typing import List, Optional, Dict
from fastapi_camelcase import CamelModel
from inference_tools.type import RuleType
from pydantic import BaseModel


class InputParameter(BaseModel):
    """An input parameter of a rule"""
    name: str
    values: Optional[List[str]] = None  # valid values
    description: str


class EmbeddingModel(BaseModel):
    """An embedding model in a rule"""
    description: str
    name: str
    distance: str
    id: str


class RuleOutput(CamelModel):
    """A data generalization rule output"""
    id: str
    name: str
    description: str
    resource_type: str
    input_parameters: List[InputParameter]
    nexus_link: str
    embedding_models: Dict[str, EmbeddingModel]


class RuleInput(BaseModel):
    """A data generalization rule input"""
    id: str


class RulesBody(CamelModel):
    """Request body for rules"""
    resource_types: Optional[List[str]] = None
    resource_id: Optional[str] = None
    input_filters: Optional[dict] = None
    rule_types: Optional[List[RuleType]] = None

