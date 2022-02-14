from models.rules import InputParameter, Rule
from inference_tools.utils import get_rule_parameters


class Serializer:
    """The serializer class"""

    @staticmethod
    def serialize_rules(rules: list):
        """
        Serializes a list of data generalization rules by returning their models

        :param rules: the list of rules
        :return:
        """
        serialized_rules = []
        for rule in rules:
            params = get_rule_parameters(rule)
            print("Input parameters: ")
            input_parameters = []
            # loop over the input parameters
            for name, payload in params.items():
                input_parameters.append(InputParameter(name=name, payload=payload))
            rule = Rule(name=rule["name"],
                        description=rule["description"],
                        targetResourceType=rule["targetResourceType"],
                        inputParameters=input_parameters)
            serialized_rules.append(rule)
        return serialized_rules
