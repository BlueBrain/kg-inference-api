import logging
from typing import List
from inference_tools.utils import check_premises, get_query_pipe_params
from api.models.rules import InputParameter, RuleOutput
from api.session import UserSession
from inference_tools.exceptions import InferenceToolsException


class RulesHandler:
    """A class to manage the rules and their actions"""

    def __init__(self, rules: List[dict]) -> None:
        self.rules = rules

    def filter_rules(self, input_filters: dict, user_session: UserSession):
        """
        Filter the rules that satisfy all the input filters

        :param user_session:
        :param input_filters:
        :return:
        """

        def rule_is_satisfied(rule):
            return check_premises(forge_factory=user_session.get_or_create_forge_session,
                                  rule=rule,
                                  parameters=input_filters)

        self.rules = [rule for rule in self.rules if rule_is_satisfied(rule)]

    def serialize_rules(self):
        """
        Serializes a list of data generalization rules by returning their models

        :return:
        """
        serialized_rules = []
        for rule in self.rules:
            try:
                params = get_query_pipe_params(rule["searchQuery"])
            except (KeyError, InferenceToolsException):
                logging.exception(f'Rule \"{rule["name"]}\" could not be parsed')
                continue

            input_parameters = [InputParameter(name=name, payload=payload)
                                for name, payload in params.items()] if params else []

            rule = RuleOutput(id=rule["@id"] if "@id" in rule else rule["id"],
                              name=rule["name"],
                              description=rule["description"],
                              resource_type=rule["targetResourceType"],
                              input_parameters=input_parameters,
                              nexus_link=rule["nexus_link"])

            serialized_rules.append(rule)

        return serialized_rules
