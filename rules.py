from typing import List
from inference_tools.utils import get_rule_parameters, check_premises
from pydantic import Json
from models.rules import InputParameter, Rule


class RulesHandler:
    """A class to manage the rules and their actions"""

    def __init__(self, rules: List[dict]) -> None:
        self.rules = rules

    def filter_rules(self, input_filters: List[Json], token: str):
        """
        Filter the rules that satisfy all the input filters

        :param input_filters:
        :param token:
        :return:
        """
        satisfied_rules = []
        for rule in self.rules:
            rule_is_satisfied = True
            for input_filter in input_filters:
                if not check_premises(rule, input_filter, token):
                    rule_is_satisfied = False
                    break
            if rule_is_satisfied:
                satisfied_rules.append(rule)
        self.rules = satisfied_rules

    def serialize_rules(self):
        """
        Serializes a list of data generalization rules by returning their models

        :param rules: the list of rules
        :return:
        """
        serialized_rules = []
        for rule in self.rules:
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
