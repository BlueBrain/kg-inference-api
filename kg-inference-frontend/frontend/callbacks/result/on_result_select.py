from dash import Input, Output, State, ALL
from dash.exceptions import PreventUpdate

from data.utils import get_id


def on_result_select(app):
    @app.callback(
        Output(component_id="selected_result", component_property="data"),
        Input(component_id="datatable_results", component_property="selected_row_ids"),
        Input(component_id={
            "name": ALL,
            "index": "embedding_graph",
        }, component_property="clickData"),
        State(component_id="stored_results", component_property="data"),
        State(component_id="selected_nm", component_property="data")
    )
    def on_result_select_callback(row_select_id, point_select_id, stored_results, selected_nm):
        if row_select_id and row_select_id[0]:
            id_ = row_select_id[0]
            return stored_results[id_]
        if point_select_id and point_select_id[0]:
            id_ = point_select_id[0]["points"][0]["customdata"][0]
            if id_ == get_id(selected_nm):
                return selected_nm

            return stored_results[id_]

        raise PreventUpdate
