from dataclasses import dataclass
from data.input_parameter import InputParameter


@dataclass(init=True)
class Rule:
    id: str
    name: str
    description: str
    resource_type: str
    input_parameters: [InputParameter]
    nexus_link: str

    @staticmethod
    def class_to_store(rule):
        return {
            "id": rule.id,
            "description": rule.description,
            "name": rule.name,
            "resourceType": rule.resource_type,
            "inputParameters": [InputParameter.class_to_store(el) for el in rule.input_parameters],
            "nexusLink": rule.nexus_link
        }

    @staticmethod
    def source_to_class(rule):
        return Rule(
            id=rule["id"],
            description=rule["description"],
            name=rule["name"],
            resource_type=rule["resourceType"],
            input_parameters=[InputParameter.source_to_class(el) for el in rule["inputParameters"]],
            nexus_link=rule["nexusLink"]
        )

    @staticmethod
    def store_to_class(rule):
        return Rule(
            id=rule["id"],
            description=rule["description"],
            name=rule["name"],
            resource_type=rule["resourceType"],
            input_parameters=[InputParameter.store_to_class(el) for el in rule["inputParameters"]],
            nexus_link=rule["nexusLink"]
        )
