from typing import Dict, List
from dash import html, dcc

from layout.rule.inference_inputs import get_input_group, get_form_control, build_id


def nm_rules_input_groups(rule, token: str, sidebar_content: Dict[str, Dict],
                          stored_filters: Dict[str, List]) -> List[html.Div]:

    input_parameters = dict((i.name, i) for i in rule.input_parameters)
    param1 = input_parameters["TargetResourceParameter"]

    ig_1 = get_input_group(
        form_control=get_form_control(
            input_parameter=param1,
            sidebar_content=sidebar_content,
            stored_filters=stored_filters,
            token=token,
            rule_id=rule.id
        ),
        label=param1.description
    )

    param2 = input_parameters["IgnoreModelsParameter"]

    # key, label
    values = dict((el, el.replace("_", " ")) for el in param2.values.keys())

    ig_2 = get_input_group(
        form_control=dcc.Checklist(
            id=build_id(rule_id=rule.id, name=param2.name, control_type="opposite"),
            options=values,
            value=[]
        ),
        label="Models to use"
    )

    return [ig_1, ig_2]
