from dash import html, dcc
from dash.development.base_component import Component
from data.input_parameter import InputParameter, InputParameterType
from data.dict_key import DictKey
from data.brain_region import BrainRegion
from layout.rule.inference_inputs import get_form_control, get_input_group, build_id, get_form_control_special
from typing import List, Dict

GENERALIZE_HIERARCHY_ID = "https://bbp.epfl.ch/neurosciencegraph/data/5d04995a-6220-4e82-b847-8c3a87030e0b"

br_uri = "https://neuroshapes.org/BrainRegion"
ct_uri = "https://bbp.epfl.ch/ontologies/core/bmo/BrainCellType"

br_path = "nsg:brainLocation/nsg:brainRegion"
ct_path = ""  # TODO


def generalise_context_input_groups(rule, token: str, sidebar_content: Dict[str, Dict],
                                    stored_filters: Dict[str, List]) -> List[html.Div]:
    """

    @param rule:
    @param token: the user authentication token
    @param sidebar_content:
    @param stored_filters:
    @return
    """
    # TypeQueryParameter
    i_f = InputParameter(name="TypeQueryParameter", type=InputParameterType.PATH,
                         description="", optional=False)

    control1 = get_input_group(form_control=get_form_control(
        input_parameter=i_f, rule_id=rule.id, token=token,
        sidebar_content=sidebar_content, stored_filters=stored_filters),
        label="Result Type"
    )

    # GeneralizedFieldName
    control2 = get_input_group(
        form_control=dcc.RadioItems(
            options={
                ct_uri: "Cell Type",
                br_uri: "Brain Region"
            },
            inline=True,
            value=br_uri,
            id=build_id(rule_id=rule.id, name="GeneralizedFieldName")
        ),
        label="Hierarchy to use for generalisation"
    )

    # GeneralizedFieldValue
    control3 = html.Div(id="variable_dropdown", children=update_generalized_field_value(
        rule_id=rule.id, token=token, dict_key=DictKey.BRAIN_REGIONS.value,
        class_name=BrainRegion, sidebar_content=sidebar_content,
        stored_filters=stored_filters)
                        )

    # SearchDown
    control4 = get_input_group(form_control=dcc.RadioItems(
        options=[{"value": "false", "label": "Up"}, {"value": "true", "label": "Down"}],
        inline=True,
        value="false",
        id=build_id(rule_id=rule.id, name="SearchDown")
    ), label="Generalisation direction")

    # PathToGeneralizedField
    control5 = dcc.Input(disabled=True, id=build_id(rule_id=rule.id, name="PathToGeneralizedField"), value=br_path)

    # UserContext: ignore

    return [control1, control2, control3, control4, control5]


def update_generalized_field_value(rule_id: str, token: str, dict_key: str, class_name,
                                   sidebar_content: Dict[str, Dict], stored_filters: Dict[str, List]) -> html.Div:
    """

    @param rule_id:
    @param token:
    @param dict_key:
    @param class_name:
    @param sidebar_content:
    @param stored_filters:
    @return
    """
    return get_input_group(
        form_control=get_form_control_special(
            class_name=class_name,
            id_obj=build_id(rule_id=rule_id, name="GeneralizedFieldValue"),
            multiple=False,
            token=token,
            dict_key=dict_key, stored_filters=stored_filters, sidebar_content=sidebar_content),
        label="Hierarchy starting value"
    )
