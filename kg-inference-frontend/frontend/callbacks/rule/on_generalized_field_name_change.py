from dash import Input, Output, State, ALL
from dash.exceptions import PreventUpdate

from callbacks.auth.on_stored_token_sidebar_filter import GENERALIZE_SIMILARITY_ID
from data.rule import Rule
from layout.rule.custom_rules.generalize_hierarchy_rule import GENERALIZE_HIERARCHY_ID, \
    update_generalized_field_value, value_map
from layout.rule.custom_rules.generalize_similarity_rule import build_from_sub_rule
from layout.rule.inference_inputs import build_id
from data.dict_key import dict_key_class_map, DictKey


def on_generalized_field_name_change(app):
    @app.callback(
        Output(component_id="hierarchy_generalized_field_value_container",
               component_property="children"),
        Output(component_id="exclude_query_parameter_container", component_property="children"),
        Input(component_id={
            "type": "infer_form_control",
            "name": "GeneralizedFieldName",
            "index": GENERALIZE_HIERARCHY_ID,
            "control_type": "basic"
        }, component_property="value"),
        State(component_id="selected_rule", component_property="data"),
        State(component_id="sidebar_content", component_property="data"),
        State(component_id="stored_token", component_property="data"),
        State(component_id="stored_filters", component_property="data")
    )
    def on_hierarchy_generalized_field_name_change_callback(
            new_field_name, selected_rule, sidebar_content, token, stored_filters):
        if not new_field_name:
            raise PreventUpdate

        dict_key = value_map[new_field_name]["dict_key"]
        class_name = dict_key_class_map[dict_key]

        rule_id = selected_rule["id"]

        control1 = update_generalized_field_value(
            id_obj=build_id(rule_id=rule_id, name="GeneralizedFieldValue"),
            token=token,
            dict_key=dict_key,
            class_name=class_name,
            sidebar_content=sidebar_content,
            stored_filters=stored_filters,
            label="Hierarchy starting value",
            multiple=False
        )

        control2 = update_generalized_field_value(
            id_obj=build_id(rule_id=rule_id, name="ExcludeQueryParameter"),
            token=token,
            dict_key=dict_key,
            class_name=class_name,
            sidebar_content=sidebar_content,
            stored_filters=stored_filters,
            label="Elements to exclude",
            multiple=True
        )

        return control1, control2

    @app.callback(
        Output(component_id="type_query_parameter_container", component_property="children"),
        Output(component_id="similarity_generalized_field_value_container",
               component_property="children"),
        Input(component_id={
            "type": "infer_form_control",
            "name": "GeneralizedFieldName",
            "index": GENERALIZE_SIMILARITY_ID,
            "control_type": "basic"
        }, component_property="value"),
        State(component_id='selected_rule', component_property='data'),
        State(component_id="sidebar_content", component_property="data"),
        State(component_id="stored_token", component_property="data"),
        State(component_id="stored_filters", component_property="data")
    )
    def on_hierarchy_generalized_field_name_change_callback(
            new_field_name, selected_rule, sidebar_content, token, stored_filters
    ):

        if not new_field_name:
            raise PreventUpdate

        return build_from_sub_rule(
            hierarchy_dict_key=DictKey(new_field_name),
            rule=Rule.store_to_class(selected_rule),
            token=token,
            sidebar_content=sidebar_content,
            stored_filters=stored_filters
        )
