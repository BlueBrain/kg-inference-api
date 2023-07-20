from dash import Input, Output, no_update, State, ALL

from data.result.result_resource import ResultResource
from layout.utils import ToastType, make_toast, grey_box
from layout.result.result_list import build_result_list


def on_stored_results_update(app):
    @app.callback(
        Output(component_id="prepared_plot_data", component_property="data"),
        Output(component_id="result_list", component_property="children"),
        Output(component_id="toast_container_results_table", component_property="children"),
        Input(component_id="stored_results", component_property="data"),
        State(component_id="selected_rule", component_property="data"),
        State(component_id="stored_token", component_property="data"),
        State(component_id="selected_nm", component_property="data"),
        prevent_initial_call=True
    )
    def on_stored_results_update_callback(results, rule, token, selected_nm):
        if results is None:
            return None, grey_box(), no_update

        selected_nm = ResultResource.store_to_class(selected_nm) \
            if selected_nm is not None else None

        prepared_plot_data, list_div = build_result_list(
            results, rule=rule, token=token,
            selected_nm=selected_nm
        )

        return (
            prepared_plot_data,
            list_div,
            make_toast(ToastType.INFORMATION, f"Results displayed")
        )
