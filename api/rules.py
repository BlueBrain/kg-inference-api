import logging
from typing import List
from inference_tools.utils import get_rule_parameters, check_premises
from pydantic import Json
from api.models.rules import InputParameter, RuleOutput
from api.session import UserSession


class RulesHandler:
    """A class to manage the rules and their actions"""

    def __init__(self, rules: List[dict]) -> None:
        self.rules = rules

    def filter_rules(self, input_filters: List[Json], user_session: UserSession):
        """
        Filter the rules that satisfy all the input filters

        :param user_session:
        :param input_filters:
        :return:
        """
        satisfied_rules = []
        for rule in self.rules:
            rule_is_satisfied = True
            for input_filter in input_filters:
                if not check_premises(forge_factory=user_session.get_or_create_forge_session,
                                      rule=rule,
                                      parameters=input_filter):
                    rule_is_satisfied = False
                    break
            if rule_is_satisfied:
                satisfied_rules.append(rule)
        self.rules = satisfied_rules

    def serialize_rules(self):
        """
        Serializes a list of data generalization rules by returning their models

        :return:
        """
        serialized_rules = []
        for rule in self.rules:
            try:
                params = get_rule_parameters(rule)
                input_parameters = []
                # loop over the input parameters
                for name, payload in params.items():
                    input_parameters.append(InputParameter(name=name, payload=payload))
                rule = RuleOutput(id=rule["@id"],
                                  name=rule["name"],
                                  description=rule["description"],
                                  resource_type=rule["targetResourceType"],
                                  input_parameters=input_parameters)
                serialized_rules.append(rule)
            except KeyError:
                logging.exception('Rule with id '+rule["name"] + ' could not be parsed')
        return serialized_rules
