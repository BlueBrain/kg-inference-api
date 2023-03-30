from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from layout.result.result_chart import build_result_chart


def on_chart_control_change(app):
    @app.callback(
        Output(component_id='chart_container', component_property='children'),
        Input(component_id="chart_button", component_property="n_clicks"),
        State(component_id="x_axis_chart", component_property="value"),
        State(component_id="y_axis_chart", component_property="value"),
        State(component_id="stored_results", component_property="data"),
    )
    def on_chart_control_change_callback(n_clicks, x_axis_select, y_axis_select, stored_results):
        if n_clicks and n_clicks > 0:
            return build_result_chart(stored_results.values(), x_axis=x_axis_select,
                                      y_axis=y_axis_select)

        raise PreventUpdate
