from dash import Input, Output, State, no_update
from dash.exceptions import PreventUpdate
from layout.utils import make_toast, ToastType


def on_auth_press(app):
    @app.callback(
        Output(component_id="stored_token", component_property="data"),
        Output(component_id="toast_container_token", component_property="children"),
        Input(component_id="save_token_button", component_property="n_clicks"),
        State(component_id="token_input", component_property="value")
    )
    def on_auth_press_callback(n_clicks, token_input):
        if n_clicks and n_clicks > 0:

            if token_input != "" and token_input is not None:
                return (
                    token_input,
                    make_toast(ToastType.INFORMATION, "Token saved")
                )

            return (
                no_update,
                make_toast(ToastType.WARNING, "Empty Token"),
            )

        raise PreventUpdate
