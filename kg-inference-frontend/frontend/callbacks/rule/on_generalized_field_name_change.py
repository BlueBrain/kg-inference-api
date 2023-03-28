from dash import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
from layout.rule.custom_rules.generalize_hierarchy_rule import GENERALIZE_HIERARCHY_ID,\
    update_generalized_field_value, value_map
from layout.rule.inference_inputs import build_id


def on_generalized_field_name_change(app):
    @app.callback(
        Output(component_id="generalized_field_value_container", component_property="children"),
        Output(component_id="exclude_query_parameter_container", component_property="children"),
        Input(component_id={
            "type": "infer_form_control",
            "name": "GeneralizedFieldName",
            "index": GENERALIZE_HIERARCHY_ID,
            "control_type": "basic"
        }, component_property="value"),
        State(component_id='selected_rule', component_property='data'),
        State(component_id="sidebar_content", component_property="data"),
        State(component_id="stored_token", component_property="data"),
        State(component_id="stored_filters", component_property="data")
    )
    def on_generalized_field_name_change_callback(new_field_name, selected_rule, sidebar_content,
                                                  token, stored_filters):
        if not new_field_name:
            raise PreventUpdate

        dict_key = value_map[new_field_name]["dict_key"]
        class_name = value_map[new_field_name]["class_name"]

        rule_id = selected_rule["id"]

        control1 = update_generalized_field_value(
                id_obj=build_id(rule_id=rule_id, name="GeneralizedFieldValue"),
                token=token, dict_key=dict_key,
                class_name=class_name, sidebar_content=sidebar_content,
                stored_filters=stored_filters,
                label="Hierarchy starting value",
                multiple=False
            )

        control2 = update_generalized_field_value(
                id_obj=build_id(rule_id=rule_id, name="ExcludeQueryParameter"),
                token=token, dict_key=dict_key,
                class_name=class_name, sidebar_content=sidebar_content,
                stored_filters=stored_filters,
                label="Elements to exclude",
                multiple=True
            )

        return control1, control2
