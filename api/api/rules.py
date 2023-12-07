"""
Module: rules_handler.py

This module defines the RulesHandler class for managing rules and their actions.
"""
import dataclasses
from typing import List, Dict, Union
from inference_tools.datatypes.rule import Rule
from api.models.rules import InputParameter, RuleOutput


@dataclasses.dataclass
class RulesHandler:
    """
    A class to manage the rules and their actions.
    """

    rules: Union[List[Rule], Dict[str, List[Rule]]]

    def __init__(self, rules: Union[List[Rule], Dict[str, List[Rule]]]) -> None:
        """
        Initializes a new RulesHandler instance with the provided rules.

        Parameters:
            - rules (Union[List[Rule], Dict[str, List[Rule]]]): The rules to be managed.
        """
        self.rules = rules

    def serialize_rules(self) -> Union[List[RuleOutput], List[Dict]]:
        """
        Serializes a list of data generalization rules by returning their models.

        Returns:
            Union[List[RuleOutput], List[Dict]]: List of serialized RuleOutput models or dictionaries.
        """

        def format_list(rule_list: List[Rule]) -> List[RuleOutput]:
            """
            Formats a list of Rule objects into a list of RuleOutput models.

            Parameters:
                - rule_list (List[Rule]): The list of Rule objects to be formatted.

            Returns:
                List[RuleOutput]: List of formatted RuleOutput models.
            """
            return [
                rule
                for rule in map(
                    lambda rule: RuleOutput(
                        id=rule.id,
                        name=rule.name,
                        description=rule.description,
                        resource_type=rule.target_resource_type,
                        input_parameters=[
                            InputParameter(
                                name=ip.name,
                                description=ip.description,
                                values=ip.values,
                            )
                            for ip in rule.flattened_input_parameters
                        ],
                        nexus_link=rule.nexus_link,
                    ),
                    rule_list,
                )
                if rule is not None
            ]

        if isinstance(self.rules, list):
            return format_list(self.rules)

        return [{"resource_id": res_id, "rules": format_list(rule_list)} for (res_id, rule_list) in self.rules.items()]
