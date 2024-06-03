"""
Module: rules_models.py

This module defines Pydantic models for handling rules-related requests and responses.
"""

from typing import List, Optional, Dict, Any, Union
from fastapi_camelcase import CamelModel
from inference_tools.type import RuleType
from pydantic import BaseModel


class InputParameter(BaseModel):
    """
    An input parameter of a rule.

    Attributes:
        - name (str): The name of the input parameter.
        - values (Optional[Dict[str, Any]]): Optional dictionary of parameter values.
        - description (str): The description of the input parameter.

    """

    name: str
    values: Optional[Dict[str, Any]] = None
    description: str


class EmbeddingModel(BaseModel):
    """
    An embedding model in a rule.

    Attributes:
        - description (str): The description of the embedding model.
        - name (str): The name of the embedding model.
        - distance (str): The distance metric associated with the embedding model.
        - id (str): The identifier of the embedding model.

    """

    description: str
    name: str
    distance: str
    id: str


class RuleOutput(CamelModel):
    """
    A data generalization rule output.

    Attributes:
        - id (str): The identifier of the rule.
        - name (str): The name of the rule.
        - description (str): The description of the rule.
        - resource_type (str): The resource type associated with the rule.
        - input_parameters (List[InputParameter]): List of input parameters for the rule.
        - nexus_link (str): The Nexus link associated with the rule.

    """

    id: str
    name: str
    description: str
    resource_type: str
    input_parameters: List[InputParameter]
    nexus_link: str


class RuleInput(BaseModel):
    """
    A data generalization rule input.

    Attributes:
        - id (str): The identifier of the rule.

    """

    id: str


class RulesBody(CamelModel):
    """
    Request body for rules.

    Attributes:
        - resource_types (Optional[List[str]]): Optional list of resource types.
        - resource_ids (Optional[Union[str, List[str]]]): Optional union of a single or list of resource IDs.
        - input_filters (Optional[dict]): Optional dictionary representing input filters.
        - rule_types (Optional[List[RuleType]]): Optional list of rule types.

    """

    resource_types: Optional[List[str]] = None
    resource_ids: Optional[Union[str, List[str]]] = None
    input_filters: Optional[dict] = None
    rule_types: Optional[List[RuleType]] = None
