from dash import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
from data.brain_region import BrainRegion
from data.cell_type import CellType
from data.dict_key import DictKey
from layout.rule.custom_rules.generalize_hierarchy_rule import GENERALIZE_HIERARCHY_ID, br_uri, br_path, \
    ct_uri, ct_path, update_generalized_field_value


def on_generalized_field_name_change(app):
    @app.callback(
        Output(component_id="variable_dropdown", component_property="children"),
        Output(component_id={
            "type": "infer_form_control",
            "name": "PathToGeneralizedField",
            "index": ALL,  # for some reason doesn't work when specifying id
            "control_type": "basic"
        }, component_property="value"),
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
    def on_generalized_field_name_change_callback(new_field_name, selected_rule, sidebar_content, token,
                                                  stored_filters):
        if not new_field_name:
            raise PreventUpdate

        if new_field_name == br_uri:
            dict_key, class_name, path = DictKey.BRAIN_REGIONS.value, BrainRegion, br_path
        elif new_field_name == ct_uri:
            dict_key, class_name, path = DictKey.CELL_TYPES.value, CellType, ct_path
        else:
            raise ValueError

        return update_generalized_field_value(rule_id=selected_rule["id"], class_name=class_name,
                                              dict_key=dict_key, token=token,
                                              stored_filters=stored_filters,
                                              sidebar_content=sidebar_content), [path]
        # array that must have the size of the pattern matching outputs
