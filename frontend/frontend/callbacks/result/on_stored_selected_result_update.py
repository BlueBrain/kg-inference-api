from dash import no_update, Input, Output, State, html
from layout.result.selected_result import build_selected_result
from layout.utils import grey_box


def on_stored_selected_result_update(app):
    @app.callback(
        Output(component_id="selected_result_view", component_property="children"),
        Output(component_id="selected_result_title", component_property="children"),
        Output(component_id="selected_result_loader", component_property="children"),
        Input(component_id="selected_result", component_property="data"),
        State(component_id="stored_token", component_property="data")
    )
    def on_stored_selected_result_update_callback(result, token):
        if result is not None:
            content, title = build_selected_result(result, token, app)
            return content, title, no_update

        return grey_box(), html.H5("Selected Result"), no_update
