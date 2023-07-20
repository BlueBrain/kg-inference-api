from typing import List, Dict
from fastapi_camelcase import CamelModel
from pydantic import BaseModel
from api.models.rules import RuleInput


class InferenceResult(BaseModel):
    """An inference result of a rule"""
    rule: str
    results: List[Dict]


class InferenceBody(CamelModel):
    """The body of the infer requests"""
    rules: List[RuleInput]
    input_filter: dict
