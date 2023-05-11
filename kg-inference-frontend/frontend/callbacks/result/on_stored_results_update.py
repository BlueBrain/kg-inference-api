from dash import Input, Output, no_update, State
from layout.utils import ToastType, make_toast, grey_box
from layout.result.result_list import build_result_list


def on_stored_results_update(app):

    @app.callback(
        Output(component_id="result_list", component_property="children"),
        Output(component_id="toast_container_results_table", component_property="children"),
        Input(component_id="stored_results", component_property="data"),
        State(component_id="selected_rule", component_property="data")
    )
    def on_stored_results_update_callback(results, rule):
        if results is not None:
            return build_result_list(results.values(), rule=rule), make_toast(
                ToastType.INFORMATION, f"Results displayed")

        return grey_box(), no_update
