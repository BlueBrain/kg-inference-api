from typing import List
from fastapi_camelcase import CamelModel
from pydantic import BaseModel
from models.rules import RuleInput


class Resource(BaseModel):
    """A simplified serialization of a resource"""
    id: str


class InferenceResult(BaseModel):
    """An inference result of a rule"""
    rule: str
    results: List[Resource]


class InferenceBody(CamelModel):
    """The body of the infer requests"""
    rules: List[RuleInput]
    input_filter: dict
