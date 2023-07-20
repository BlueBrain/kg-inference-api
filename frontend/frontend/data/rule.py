from dataclasses import dataclass
from typing import Optional, Dict

from data.dict_key import DictKey
from data.input_parameter import InputParameter


@dataclass(init=True)
class Rule:
    id: str
    name: str
    description: str
    resource_type: str
    input_parameters: [InputParameter]
    nexus_link: Optional[str]
    sub_rules: Optional[Dict[DictKey, Dict[str, 'Rule']]]

    @staticmethod
    def class_to_store(rule):
        return {
            "id": rule.id,
            "description": rule.description,
            "name": rule.name,
            "resourceType": rule.resource_type,
            "inputParameters": [InputParameter.class_to_store(el) for el in rule.input_parameters],
            "nexusLink": rule.nexus_link,
            "sub_rules": dict(
                (att.value, dict(
                    (m, Rule.class_to_store(r))
                    for m, r in d.items()
                ))
                for att, d in rule.sub_rules.items()
            )
            if rule.sub_rules is not None else None
        }

    @staticmethod
    def source_to_class(rule):
        return Rule(
            id=rule["id"],
            description=rule["description"],
            name=rule["name"],
            resource_type=rule["resourceType"],
            input_parameters=[InputParameter.source_to_class(el) for el in rule["inputParameters"]],
            nexus_link=rule["nexusLink"],
            sub_rules=None
        )

    @staticmethod
    def store_to_class(rule):
        return Rule(
            id=rule["id"],
            description=rule["description"],
            name=rule["name"],
            resource_type=rule["resourceType"],
            input_parameters=[InputParameter.store_to_class(el) for el in rule["inputParameters"]],
            nexus_link=rule["nexusLink"],
            sub_rules=dict(
                (
                    DictKey(att),
                    dict(
                        (m, Rule.store_to_class(r))
                        for m, r in d.items()
                    )

                ) for att, d in rule["sub_rules"].items()
            )
            if rule["sub_rules"] is not None else None
        )
