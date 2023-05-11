from typing import Any, Optional

import dash
from dash import Input, Output, State, no_update, ALL, callback_context
from dash.exceptions import PreventUpdate

from layout.rule.custom_rules.generalize_hierarchy_rule import GENERALIZE_HIERARCHY_ID, value_map
from layout.utils import make_toast, ToastType
from layout.rule.inference_inputs import DEFAULT_LIMIT
from data.rule import Rule
from query.api import infer, APIError
from query.forge import ForgeError


def on_infer_press(app):
    @app.callback(
        Output(component_id="input_parameters", component_property="data"),
        Output(component_id="toast_container_infer_press", component_property="children"),
        Input(component_id='infer_button', component_property='n_clicks'),
        State(component_id="selected_rule", component_property="data"),
        State(component_id={
            'type': 'infer_form_control',
            "name": ALL,
            "index": ALL,
            "control_type": ALL
        }, component_property='value')
    )
    def on_infer_press_callback(infer_n_clicks, rule, values):

        if not infer_n_clicks or infer_n_clicks == 0:
            raise PreventUpdate

        rule = Rule.store_to_class(rule)

        infer_form_controls = callback_context.states_list[1]
        form_control_ids = [fc["id"] for fc in infer_form_controls]
        form_control_names = [fc_id["name"] for fc_id in form_control_ids]

        # idx_limit = form_control_names.index('LimitQueryParameter')
        # limit = values[idx_limit]
        #
        # if limit is None or limit == "":
        #     limit = DEFAULT_LIMIT
        #     values[idx_limit] = limit

        form_control_types = [fc_id["control_type"] for fc_id in form_control_ids]

        i_ps = dict((i_p.name, i_p) for i_p in rule.input_parameters)
        # TODO would be better to somehow have a data_ attribute in the form control
        form_control_data = [i_ps[fc_data].values for fc_data in form_control_names]

        def format_value(value: Any, control_type: str, additional_data: Optional[Any]):
            """
            Reformatting of the values input in the form controls:
            - newline_separated: if a parameter allows for multiple values, but there is no
            predefined list of valid values for it, they are given by the user in a text area,
            and individual values are separated by a newline. The reformatting separates them
            into an array of values
            - opposite: given a form control that has a list of valid values, the user
            chooses amongst them. The values that will be submitted are all valid values
            that have NOT been selected by the user
            """
            if control_type == "basic":
                return value
            if control_type == "newline_separated":
                return value.split("\n") if value else []
            if control_type == "opposite":
                return list(set(additional_data.keys()).difference(set(value)))
            raise Exception(f"Unknown form control type {control_type}")

        values = [
            format_value(value, control_type, data)
            for (value, control_type, data) in
            zip(values, form_control_types, form_control_data)
        ]

        input_parameters = dict(zip(form_control_names, values))
        input_parameters["LimitQueryParameter"] = DEFAULT_LIMIT

        if rule.id == GENERALIZE_HIERARCHY_ID:
            selected_hierarchy = input_parameters["GeneralizedFieldName"]
            to_add = dict(list(value_map[selected_hierarchy].items())[1:])
            input_parameters.update(to_add)

        return input_parameters, make_toast(ToastType.INFORMATION, f"Started inference")

    @app.callback(
        Output(component_id="collapse_nm", component_property="className", allow_duplicate=True),
        Input(component_id='button_collapse_nm', component_property='n_clicks'),
        Input(component_id="input_parameters", component_property="data"),
        State(component_id="collapse_nm", component_property="className"),
        prevent_initial_call=True
    )
    def on_collapse_nm_click(btn_collapse_n_clicks, input_parameter, collapsed_state):
        hide_cls = "card-body collapse"
        show_cls = f"{hide_cls} show"
        if btn_collapse_n_clicks and btn_collapse_n_clicks > 0:
            return show_cls if collapsed_state == hide_cls else hide_cls

    @app.callback(
        Output(component_id="stored_results", component_property="clear_data"),
        Output(component_id="selected_result", component_property="clear_data"),
        Output(component_id="collapse_nm", component_property="className"),
        Input(component_id="input_parameters", component_property="data"),
    )
    def on_input_parameter_store(input_parameters):
        hide_cls = "card-body collapse"
        return True, True, hide_cls

    @app.callback(
        # clearing the stored_results should clear the selected result
        Output(component_id="stored_results", component_property="data"),
        Output(component_id="result_fetching_loader", component_property="children"),
        Output(component_id="toast_container_results_infer", component_property="children"),
        Input(component_id='stored_results', component_property='clear_data'),
        State(component_id="input_parameters", component_property="data"),
        State(component_id="stored_token", component_property="data"),
        State(component_id="selected_rule", component_property="data"),
    )
    def on_stored_result_clear(stored_results, input_parameters, token, rule):

        if input_parameters is not None:
            try:
                results = infer(rule_id=rule["id"], input_parameters=input_parameters, token=token)

            except (APIError, ForgeError) as e:
                return None, no_update, make_toast(ToastType.ERROR, str(e))

            return results, no_update, make_toast(
                ToastType.INFORMATION, f"Inferred {len(results)} results, building table...")

        if input_parameters is None:
            return None, no_update, no_update
