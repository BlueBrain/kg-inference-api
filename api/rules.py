import logging
from typing import List

from inference_tools.datatypes.rule import Rule
from inference_tools.execution import check_premises
from inference_tools.utils import get_search_query_parameters
from inference_tools.exceptions.exceptions import InferenceToolsException
from api.models.rules import InputParameter, RuleOutput
from api.session import UserSession


class RulesHandler:
    """A class to manage the rules and their actions"""

    rules: List[Rule]

    def __init__(self, rules: List[Rule]) -> None:
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
                                  parameter_values=input_filters)

        self.rules = [rule for rule in self.rules if rule_is_satisfied(rule)]

    def serialize_rules(self) -> List[RuleOutput]:
        """
        Serializes a list of data generalization rules by returning their models
        :return:
        """

        def rule_formatting(rule: Rule):
            try:
                input_parameters = [
                    InputParameter(name=name, payload=payload)
                    for name, payload in get_search_query_parameters(rule).items()
                ]
            except InferenceToolsException:
                logging.exception(f'Rule \"{rule.name}\" could not be parsed')
                return None

            return RuleOutput(id=rule.id,
                              name=rule.name,
                              description=rule.description,
                              resource_type=rule.target_resource_type,
                              input_parameters=input_parameters,
                              nexus_link=rule.nexus_link)

        rules = [rule_formatting(rule) for rule in self.rules]
        return [rule for rule in rules if rule is not None]
