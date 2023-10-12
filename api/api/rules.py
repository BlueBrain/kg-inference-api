from typing import List, Dict, Union

from inference_tools.datatypes.rule import Rule
from api.models.rules import InputParameter, RuleOutput


class RulesHandler:
    """A class to manage the rules and their actions"""

    rules: Union[List[Rule], Dict[str, List[Rule]]]

    def __init__(self, rules: Union[List[Rule], Dict[str, List[Rule]]]) -> None:
        self.rules = rules

    def serialize_rules(self) -> Union[List[RuleOutput], List[Dict]]:
        """
        Serializes a list of data generalization rules by returning their models
        :return:
        """

        def format_list(rule_list: List[Rule]) -> List[RuleOutput]:
            return [
                rule
                for rule in map(lambda rule: RuleOutput(
                    id=rule.id,
                    name=rule.name,
                    description=rule.description,
                    resource_type=rule.target_resource_type,
                    input_parameters=[
                        InputParameter(
                            name=ip.name, description=ip.description, values=ip.values
                        )
                        for ip in rule.flattened_input_parameters
                    ],
                    nexus_link=rule.nexus_link
                ), rule_list)
                if rule is not None
            ]

        if isinstance(self.rules, list):
            return format_list(self.rules)

        return [
            {
                "resource_id": res_id,
                "rules": format_list(rule_list)
            }
            for (res_id, rule_list) in self.rules.items()
        ]
