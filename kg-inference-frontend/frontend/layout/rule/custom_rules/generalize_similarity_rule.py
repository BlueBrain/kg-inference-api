import os
import json

from dash import html, dcc

from data.dict_key import DictKey, dict_key_class_map, dict_key_attribute_map
from data.rule import Rule
from layout.rule.inference_inputs import get_form_control, get_input_group, build_id, \
    get_form_control_special
from typing import List, Dict

DEFAULT_SIMILARITY = DictKey.BRAIN_REGIONS

field_name_map = {
    DictKey.BRAIN_REGIONS: "BrainRegionQueryParameter"
}


def generalise_similarity_input_groups(rule: Rule, token: str, sidebar_content: Dict[str, Dict],
                                       stored_filters: Dict[str, List]) -> List[html.Div]:
    """

    @param rule:
    @param token: the user authentication token
    @param sidebar_content:
    @param stored_filters:
    @return
    """

    control1, control3 = build_from_sub_rule(
        hierarchy_dict_key=DEFAULT_SIMILARITY,
        rule=rule,
        token=token,
        sidebar_content=sidebar_content,
        stored_filters=stored_filters
    )

    control1 = html.Div(
        id="type_query_parameter_container",  # TODO maybe not
        children=control1
    )

    control3 = html.Div(
        id="similarity_generalized_field_value_container",
        children=control3
    )

    control2 = get_input_group(
        form_control=dcc.RadioItems(
            options=dict(
                (dict_key.value, dict_key_attribute_map[dict_key].value)
                for dict_key in rule.sub_rules.keys()
            ),
            value=DEFAULT_SIMILARITY.value,
            inline=True,
            id=build_id(rule_id=rule.id, name="GeneralizedFieldName"),
            labelStyle={"paddingRight": "10px"}
        ),
        label="Hierarchy to use for generalisation"
    )

    return [control1, control2, control3]


def build_from_sub_rule(hierarchy_dict_key: DictKey, rule: Rule, token: str,
                        sidebar_content: Dict[str, Dict], stored_filters: Dict[str, List]):
    sub_rule = rule.sub_rules[hierarchy_dict_key]

    input_parameters = dict((i.name, i) for i in sub_rule.input_parameters)

    # TypeQueryParameter
    type_control = get_input_group(
        form_control=get_form_control(
            input_parameter=input_parameters["TypeQueryParameter"],
            rule_id=sub_rule.id,
            token=token,
            sidebar_content=sidebar_content,
            stored_filters=stored_filters
        ),
        label="Result Type"
    )

    if hierarchy_dict_key == DictKey.BRAIN_REGIONS:
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               "../../../assets/", "brain_region_ids.json"), "r") as f:
            filter_set = json.load(f)
            filter_set = [f"http://api.brain-map.org/api/v2/data/Structure/{e}" for e in filter_set]
    else:
        filter_set = None

    starting_value_control = get_input_group(
        form_control=get_form_control_special(
            dict_key=hierarchy_dict_key,
            multiple=False,
            token=token,
            sidebar_content=sidebar_content,
            stored_filters=stored_filters,
            class_name=dict_key_class_map[hierarchy_dict_key],
            id_obj=build_id(rule_id=sub_rule.id, name=field_name_map[hierarchy_dict_key]),
            disabled=False,
            filter_set=filter_set
        ),
        label="Hierarchy starting value"
    )

    # TODO enable support in the library
    # ExcludeQueryParameter
    # control5 = html.Div(
    #     id="exclude_query_parameter_container",
    #     children=get_input_group(
    #         form_control=dcc.Dropdown(),
    #         label="Elements to exclude"
    #     ),
    # )

    return type_control, starting_value_control
