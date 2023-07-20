from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict

from data.utils import get_type


class InputParameterType(Enum):
    STR = "str"
    SPARQL_LIST = "sparql_list"
    URI = "uri"
    LIST = "list"
    SPARQL_VALUE_URI_LIST = "sparql_value_uri_list"
    SPARQL_VALUE_LIST = "sparql_value_list"
    URI_LIST = "uri_list"
    PATH = "path"
    MULTI_PREDICATE_OBJECT_PAIR = "MultiPredicateObjectPair"
    BOOL = "bool"
    QUERY_BLOCK = "query_block"


@dataclass(init=True)
class InputParameter:
    name: str
    description: str
    type: InputParameterType
    optional: bool
    values: Optional[Dict]

    @staticmethod
    def class_to_store(input_parameter):
        return {
            "name": input_parameter.name,
            "description": input_parameter.description,
            "type": input_parameter.type.value,
            "optional": input_parameter.optional,
            "values": input_parameter.values
        }

    @staticmethod
    def source_to_class(input_parameter):
        input_parameter_payload = input_parameter["payload"]
        return InputParameter(
            name=input_parameter_payload.get("name", None),
            description=input_parameter_payload.get("description", None),
            type=InputParameterType(get_type(input_parameter_payload)),
            optional=bool(input_parameter_payload.get("optional", False)),
            values=input_parameter_payload.get("values", None)
        )

    @staticmethod
    def store_to_class(input_parameter):
        return InputParameter(
            name=input_parameter.get("name", None),
            description=input_parameter.get("description", None),
            type=InputParameterType(get_type(input_parameter)),
            optional=bool(input_parameter.get("optional", False)),
            values=input_parameter.get("values", None)
        )
