"""
Module: inference_models.py

This module defines Pydantic models for handling inference-related requests and responses.
"""
from typing import List, Dict
from fastapi_camelcase import CamelModel
from pydantic import BaseModel
from api.models.rules import RuleInput


class InferenceResult(BaseModel):
    """
    An inference result of a rule.

    Attributes:
        - rule (str): The identifier of the rule associated with the inference result.
        - results (List[Dict]): List of dictionaries representing the inference results.

    """

    rule: str
    results: List[Dict]


class InferenceBody(CamelModel):
    """
    The body of the infer requests.

    Attributes:
        - rules (List[RuleInput]): List of RuleInput objects representing the rules for inference.
        - input_filter (dict): Dictionary representing the input filter for the inference.

    """

    rules: List[RuleInput]
    input_filter: dict
