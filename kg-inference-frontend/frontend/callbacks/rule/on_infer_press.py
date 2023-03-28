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
        Output(component_id="stored_results", component_property="data"),
        Output(component_id="result_fetching_loader", component_property="children"),
        Output(component_id="toast_container_results_infer", component_property="children"),
        Input(component_id='infer_button', component_property='n_clicks'),
        State(component_id="stored_token", component_property="data"),
        State(component_id="selected_rule", component_property="data"),
        State(component_id={
            'type': 'infer_form_control',
            "name": ALL,
            "index": ALL,
            "control_type": ALL
        }, component_property='value')
    )
    def on_infer_press_callback(n_clicks, token, rule, values):
        if n_clicks and n_clicks > 0:

            infer_form_controls = callback_context.states_list[2]

            form_control_names = [fc["id"]["name"] for fc in infer_form_controls]

            # idx_limit = form_control_names.index('LimitQueryParameter')
            # limit = values[idx_limit]
            #
            # if limit is None or limit == "":
            #     limit = DEFAULT_LIMIT
            #     values[idx_limit] = limit

            form_control_types = [fc["id"]["control_type"] for fc in infer_form_controls]

            values = [value if control_type == "basic" else (value.split("\n") if value else [])
                      for (value, control_type) in zip(values, form_control_types)]

            rule = Rule.store_to_class(rule)

            input_parameters = dict(zip(form_control_names, values))
            input_parameters["LimitQueryParameter"] = DEFAULT_LIMIT

            if rule.id == GENERALIZE_HIERARCHY_ID:
                selected_hierarchy = input_parameters["GeneralizedFieldName"]
                to_add = dict(list(value_map[selected_hierarchy].items())[2:])
                input_parameters.update(to_add)

            try:
                results = infer(rule_id=rule.id, input_parameters=input_parameters, token=token)

            except (APIError, ForgeError) as e:
                print(e)
                return None, no_update, make_toast(ToastType.ERROR, str(e))

            return results, no_update, make_toast(
                ToastType.INFORMATION, f"Inferred {len(results)} results, building table...")

        raise PreventUpdate
