from dash import Input, Output, no_update, State, ALL

from data.result.result_resource import ResultResource
from layout.utils import ToastType, make_toast, grey_box
from layout.result.result_list import build_result_list
from query.forge import ForgeError, get_neuron_morphology


def on_stored_results_update(app):
    @app.callback(
        Output(component_id="prepared_plot_data", component_property="data"),
        Output(component_id="result_list", component_property="children"),
        Output(component_id="toast_container_results_table", component_property="children"),
        Output(component_id="selected_nm", component_property="data", allow_duplicate=True),
        Input(component_id="stored_results", component_property="data"),
        State(component_id="selected_rule", component_property="data"),
        State(component_id="stored_token", component_property="data"),
        State(component_id="selected_nm", component_property="data"),
        State(component_id={
            "type": "infer_form_control",
            "name": "TargetResourceParameter",
            "index": ALL,
            "control_type": "basic"
        }, component_property="value"),
        State(component_id="sidebar_content", component_property="data"),
        prevent_initial_call=True
    )
    def on_stored_results_update_callback(results, rule, token, selected_nm, selected_nm_input,
                                          sidebar_content):
        if results is None:
            return None, grey_box(), no_update, no_update

        if selected_nm is None:
            if selected_nm_input and selected_nm_input[0]:
                idx = selected_nm_input[0]
                try:
                    selected_nm = get_neuron_morphology(
                        nm_id=idx, token=token, sidebar_content=sidebar_content
                    )
                except ForgeError as e:
                    return None, no_update, make_toast(ToastType.ERROR, str(e)), no_update
            else:
                return None, no_update, make_toast(
                    ToastType.ERROR, "Couldn't get selected neuron morphology"
                ), no_update
        else:
            selected_nm = ResultResource.store_to_class(selected_nm)

        prepared_plot_data, list_div = build_result_list(
                results, rule=rule, token=token,
                selected_nm=selected_nm
        )

        return (
            prepared_plot_data,
            list_div,
            make_toast(ToastType.INFORMATION, f"Results displayed"),
            ResultResource.class_to_store(selected_nm)
        )

