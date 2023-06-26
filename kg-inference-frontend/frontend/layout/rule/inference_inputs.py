from typing import Dict, List, Optional, Any, Type
from dash import html, dcc
from dash.development.base_component import Component

from data.identifiable import Identifiable
from data.input_parameter import InputParameter, InputParameterType
from data.dict_key import DictKey, dict_key_class_map
from data.rule import Rule
from query.forge import get_forge_neuroscience_datamodels

DEFAULT_LIMIT = 50


def get_form_control_special(
        dict_key: Optional[DictKey],
        class_name: Type[Identifiable],
        multiple: bool,
        id_obj: Dict[str, str],
        token: str,
        sidebar_content: Dict[str, Dict],
        stored_filters: Dict[str, List],
        disabled: bool,
        filter_set: Optional[List[str]] = None
) -> Component:
    """
    Returns the form control for a specific set of input parameter names, those whose user
    selected value has a type that is known, and therefore whose valid values are known too and
    can be listed to the user.
    Additionally, if the form control controls a type that is one of the data types found in the
    sidebar, and the user already selected a value in the sidebar, the form control will be
    pre-filled with the sidebar selection.

    @param class_name: the data class of the values that should be listed
    @param disabled: whether the form control is disabled or not
    @param dict_key: if class_name is one of the dataclasses loaded in the sidebar, a dict key is
    specified, and it is the key into the sidebar loaded data held in sidebar_content, that will
    lead to the data that will populate the form control. If the dict key is None, then the
    dataclass is known, but the list of valid values
    is not present in the sidebar data, and it will be fetched here.
    @param multiple: whether multiple values can be selected by the form control
    @param id_obj: the id that will be attributed to the form control
    @param token: the user authentication token
    @param sidebar_content: the data that has been loaded into the sidebar.
    Some input controls will use some as a list of available values
    @param stored_filters: the filters chosen by the user in the sidebar.
    @param filter_set: a list of ids to keep from the sidebar content valid values, if not all of
    them are valid values
    Some input controls will use them to preselect a value
    @return
    """
    # class_to_func = {
    #
    # }

    def to_dropdown_format(el_list):
        return [
            {"value": el.id, "label": el.name}
            for el in el_list
        ]

    # rendering an input that is of one of the datatypes loaded in the sidebar
    if dict_key:
        dict_key_value = dict_key.value
        all_entities = sidebar_content[dict_key_value]
        all_as_class = [class_name.store_to_class(e) for e in all_entities]

        if filter_set is not None:
            all_as_class = [e for e in all_as_class if e.id in filter_set]

        # A filter for this dropdown has been selected in the sidebar
        if stored_filters and dict_key in stored_filters and \
                len(stored_filters[dict_key_value]) > 0:

            indexed_entities = dict((entity.id, entity) for entity in all_as_class)
            selected_filter = stored_filters[dict_key_value] if not multiple \
                else [stored_filters[dict_key_value][0]]
            filters_as_class = [indexed_entities[e] for e in selected_filter]
            ddf = to_dropdown_format(filters_as_class)

            return dcc.Dropdown(
                id=id_obj,
                multi=multiple,
                options=ddf,
                value=[el["value"] for el in ddf] if multiple else ddf[0]["value"],
                disabled=disabled
            )

        return dcc.Dropdown(
            id=id_obj,
            multi=multiple,
            options=to_dropdown_format(all_as_class),
            disabled=disabled
        )
    # else:  # TODO so far doesn't reach this with extraction of MType and Entity
    #
    #     if class_name in class_to_func:
    #         forge = get_forge_neuroscience_datamodels(token)
    #         data = class_to_func[class_name](forge)
    #         return dcc.Dropdown(
    #             id=id_obj,
    #             multi=multiple,
    #             options=to_dropdown_format(data),
    #             disabled=disabled
    #         )
    #
    #     raise ValueError


def build_id(rule_id, name, control_type="basic") -> Dict[str, str]:
    """
    Builds the id of a form control, as an object, in order to match the pattern of a callback.
    see: https://dash.plotly.com/pattern-matching-callbacks and
    :func:`on_infer_press_callback <callbacks.rule.on_infer_press.on_infer_press>`

    @param rule_id: the id of the rule whose input parameter's form control gets this id
    @param name: the name of the input parameter associated with the form control that will have
    this id
    @param control_type: the id contains a control_type, and the id is attributed to a form control.
    Each control type is associated with some reformatting of the value produced by the form control
    @return
    """
    return {
        "type": "infer_form_control",
        "name": name,
        "index": rule_id,
        "control_type": control_type
    }


def get_form_control(input_parameter: InputParameter, rule_id: str, token: str,
                     sidebar_content: Dict[str, Dict], stored_filters: Dict[str, List],
                     disabled=False) \
        -> Component:
    """
    Gets a form control for a rule's input parameter. For some input parameter names, the form
    control will allow for the selection of values from   a predefined list,
    see :func:`get_form_control_special<layout.rule.inference_inputs.get_form_control_special>`
    For some input parameter types, the form control will allow for selection of multiple values.

    @param input_parameter: the input parameter this form control will set the value for
    @param rule_id: the id of the rule associated with the input parameter
    @param token: the user authentication token
    @param disabled: whether to disable the form control or not
    @param sidebar_content: the data that has been loaded into the sidebar.
    Some input controls will use some as a list of available values
    @param stored_filters: the filters chosen by the user in the sidebar.
    Some input controls will use them to preselect a value
    @return a form control that will set a value for a rule's input parameter
    """

    list_types = [InputParameterType.LIST, InputParameterType.URI_LIST,
                  InputParameterType.SPARQL_LIST, InputParameterType.SPARQL_VALUE_LIST,
                  InputParameterType.SPARQL_VALUE_URI_LIST]

    multiple = input_parameter.type in list_types

    special_inputs = {
        "BrainRegionQueryParameter": DictKey.BRAIN_REGIONS,
        "BrainRegionQueryParameter_exclude": DictKey.BRAIN_REGIONS,
        "TypeQueryParameter": DictKey.DATA_TYPES,
        "MTypeQueryParameter": DictKey.M_TYPES,
        "CellTypeQueryParameter": DictKey.CELL_TYPES,
        "SpeciesQueryParameter": DictKey.SPECIES,
        "SpeciesQueryParameter_exclude": DictKey.SPECIES
    }

    if input_parameter.name in special_inputs.keys():
        dict_key = special_inputs[input_parameter.name]
        class_name = dict_key_class_map[dict_key]
        id_obj = build_id(rule_id=rule_id, name=input_parameter.name)

        return get_form_control_special(
            dict_key=dict_key,
            class_name=class_name,
            multiple=multiple,
            id_obj=id_obj,
            sidebar_content=sidebar_content,
            stored_filters=stored_filters,
            token=token,
            disabled=disabled
        )

    if input_parameter.type == InputParameterType.BOOL:
        return dcc.RadioItems(
            options={"true": "Yes", "false": "No"},
            inline=True,
            value="true",
            id=build_id(rule_id=rule_id, name=input_parameter.name),
            name=input_parameter.name,
            className="form-control"
        )  # TODO disabled?
    if multiple:
        return dcc.Textarea(
            id=build_id(rule_id=rule_id, name=input_parameter.name,
                        control_type="newline_separated"),
            name=input_parameter.name,
            className="form-control",
            disabled=disabled
        )

    return dcc.Input(
        id=build_id(rule_id=rule_id, name=input_parameter.name),
        name=input_parameter.name,
        className="form-control",
        disabled=disabled
    )


def get_input_group(form_control: Component, label: str) -> html.Div:
    """
        Creates an input group from a label and its form control, associated to a rule's input
        parameter

        @param form_control: the form control to set a value for the input parameter
        @param label: the label describing the input parameter
        @return a div with the label above the form control
    """
    return html.Div(children=[
        html.Label(children=label),  # TODO add htmlFor
        form_control,
    ], className="col mt-2")


def get_limit_form_control(rule_id: str) -> html.Div:
    """
        Builds the form group that contains the control to specify a limit of results

        @param rule_id: the id of the rule being displayed
        @return the form group that contains the control to specify a limit of results
    """
    return html.Div(className="float-end", children=[
        get_input_group(
            label="Number of Results",
            form_control=dcc.Input(type="number", id=build_id(rule_id, "LimitQueryParameter"),
                                   style={"width": "70px"},
                                   className="ms-2", value=DEFAULT_LIMIT)
        ),
        html.Small("Only the most recently updated"), html.Br(),
        html.Small(f"will be shown (if empty: {DEFAULT_LIMIT} only)")
    ])


def generic_input_groups(rule: Rule, token: str, sidebar_content: Dict[str, Dict],
                         stored_filters: Dict[str, List]) -> List[html.Div]:
    """
        Get all input groups for most rules, by iterating over the input parameters and rendering
        one for each of them. Currently, MULTI_PREDICATE_OBJECT_PAIR (additional filters set by
        the user) is not supported. An input group being a label and an input control, the input
        control is chosen according to a logic described in get_input. If a rule required
        specific handling of its input
        parameters, the input groups will be rendered by a specific function in ./custom_rules/..

        @param rule: the selected rule
        @param token: the user authentication token
        @param sidebar_content: the data that has been loaded into the sidebar.
        Some input controls will use some as a list of available values
        @param stored_filters: the filters chosen by the user in the sidebar.
        Some input controls will use them to preselect a value
        @return A list of input groups, each corresponding to an input parameter of the rule
    """
    return [
        get_input_group(
            form_control=get_form_control(
                input_parameter=input_parameter,
                sidebar_content=sidebar_content,
                stored_filters=stored_filters,
                token=token,
                rule_id=rule.id
            ),
            label=input_parameter.description
        )
        for input_parameter in rule.input_parameters
        if input_parameter.type != InputParameterType.MULTI_PREDICATE_OBJECT_PAIR
    ]
