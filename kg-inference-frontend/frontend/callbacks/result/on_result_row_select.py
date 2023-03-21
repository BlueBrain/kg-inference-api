from dash import Input, Output, State
from dash.exceptions import PreventUpdate


def on_result_row_select(app):
    @app.callback(
        Output(component_id='selected_result', component_property='data'),
        Input(component_id='datatable_results', component_property='selected_row_ids'),
        State(component_id="stored_results", component_property="data")
    )
    def on_result_row_select_callback(selected_row_ids, stored_results):
        if selected_row_ids and selected_row_ids[0]:
            idx = selected_row_ids[0]
            return stored_results[idx]

        raise PreventUpdate
