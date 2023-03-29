from dash import html, dcc

from data.cell_type import EType, MType
from data.dict_key import DictKey
from data.brain_region import BrainRegion
from data.species import Species
from layout.rule.inference_inputs import get_form_control, get_input_group, build_id, \
    get_form_control_special
from typing import List, Dict

GENERALIZE_HIERARCHY_ID = \
    "https://bbp.epfl.ch/neurosciencegraph/data/5d04995a-6220-4e82-b847-8c3a87030e0b"

value_map = {
    "BrainRegion": {  # GeneralizedFieldName
        "dict_key": DictKey.BRAIN_REGIONS,  # on GeneralizedFieldName select, this is how we find
        # the data to populate the other dropdowns
        "HierarchyRelationship": "IsPartOf",  # associated parameters values when calling the rule
        "PathToGeneralizedField": "BrainRegion"
    },
    "Species": {  # GeneralizedFieldName
        "dict_key": DictKey.SPECIES,
        "HierarchyRelationship": "SubclassOf",
        "PathToGeneralizedField": "Species"
    },
    "EType": {  # GeneralizedFieldName
        "dict_key": DictKey.E_TYPES,
        "HierarchyRelationship": "SubclassOf",
        "PathToGeneralizedField": "EType"
    },
    "MType": {  # GeneralizedFieldName
        "dict_key": DictKey.M_TYPES,
        "HierarchyRelationship": "SubclassOf",
        "PathToGeneralizedField": "MType"
    },
}

def generalise_context_input_groups(rule, token: str, sidebar_content: Dict[str, Dict],
                                    stored_filters: Dict[str, List]) -> List[html.Div]:
    """

    @param rule:
    @param token: the user authentication token
    @param sidebar_content:
    @param stored_filters:
    @return
    """

    def keys_keys(dict_instance):
        return dict(zip(dict_instance.keys(), dict_instance.keys()))

    input_parameters = dict((i.name, i) for i in rule.input_parameters)

    # TypeQueryParameter
    control1 = get_input_group(form_control=get_form_control(
        input_parameter=input_parameters["TypeQueryParameter"], rule_id=rule.id, token=token,
        sidebar_content=sidebar_content, stored_filters=stored_filters),
        label="Result Type"
    )

    # GeneralizedFieldName
    control2 = get_input_group(
        form_control=dcc.RadioItems(
            options=keys_keys(input_parameters["GeneralizedFieldName"].values),
            inline=True,
            id=build_id(rule_id=rule.id, name="GeneralizedFieldName"),
            labelStyle={"paddingRight": "10px"}
        ),
        label="Hierarchy to use for generalisation"
    )

    # GeneralizedFieldValue
    control3 = html.Div(
        id="generalized_field_value_container",
        children=get_input_group(
            form_control=dcc.Dropdown(),
            label="Hierarchy starting value"
        )
    )

    # SearchDirectionBlock
    control4 = get_input_group(
        form_control=dcc.RadioItems(
            options=keys_keys(input_parameters["SearchDirectionBlock"].values),
            inline=True,
            id=build_id(rule_id=rule.id, name="SearchDirectionBlock"),
            labelStyle={"paddingRight": "10px"}
        ),
        label="Generalisation direction"
    )

    # ExcludeQueryParameter
    control5 = html.Div(
        id="exclude_query_parameter_container",
        children=get_input_group(
            form_control=dcc.Dropdown(),
            label="Elements to exclude"
        ),
    )

    # UserContext: ignore
    # HierarchyRelationship: see on_infer_press
    # PathToGeneralizedField: see on_infer press

    return [control1, control2, control3, control4, control5]


def update_generalized_field_value(token: str, dict_key: str, class_name,
                                   sidebar_content: Dict[str, Dict],
                                   stored_filters: Dict[str, List],
                                   id_obj: Dict, label: str, multiple: bool) -> html.Div:
    """
    @param token:
    @param dict_key:
    @param class_name:
    @param sidebar_content:
    @param stored_filters:
    @param id_obj:
    @param label:
    @param multiple:
    @return
    """
    return get_input_group(
        form_control=get_form_control_special(
            class_name=class_name,
            id_obj=id_obj,
            multiple=multiple,
            token=token,
            dict_key=dict_key,
            stored_filters=stored_filters,
            sidebar_content=sidebar_content
        ),
        label=label
    )
