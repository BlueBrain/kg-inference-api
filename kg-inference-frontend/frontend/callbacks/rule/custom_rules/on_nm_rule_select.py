from dash import Input, Output, State, no_update, ALL, html
from dash.exceptions import PreventUpdate

from layout.result.result_table import build_result_table
from layout.result.selected_result import build_selected_result
from layout.utils import grey_box
from query.forge import get_neuron_morphologies


def on_nm_rule_select(app):
    @app.callback(
        Output(component_id='stored_nm', component_property='clear_data'),
        Output(component_id="selected_nm", component_property="clear_data"),
        Input(component_id='nm_container', component_property='children'),
    )
    def on_container_fill_callback(children):
        # if children is not None and len(children) > 0:
        return True, True
        # return None, no_update, True

    @app.callback(
        Output(component_id='stored_nm', component_property='data'),
        Output(component_id="nm_fetching_loader", component_property="children"),
        Input(component_id='stored_nm', component_property='clear_data'),
        State(component_id='stored_token', component_property='data'),
        State(component_id='selected_rule', component_property='data'),
    )
    def on_stored_nm_clear_data(children, token, rule):
        # if children is not None and len(children) > 0:
        return get_neuron_morphologies(token, rule["id"]), no_update
        # return None, no_update, True

    @app.callback(
        Output(component_id="nm_list", component_property="children"),
        Input(component_id='stored_nm', component_property='data')
    )
    def on_stored_nm_callback(stored_nm):
        if stored_nm is not None:
            return build_result_table(stored_nm.values(), table_id="datatable_nm")
        raise PreventUpdate

    @app.callback(
        Output(component_id='selected_nm', component_property='data'),
        Input(component_id='datatable_nm', component_property='selected_row_ids'),
        State(component_id="stored_nm", component_property="data")
    )
    def on_result_row_select_callback(selected_row_ids, stored_nm):
        if selected_row_ids and selected_row_ids[0]:
            idx = selected_row_ids[0]
            return stored_nm[idx]

        raise PreventUpdate

    @app.callback(
        Output(component_id="selected_nm_view", component_property="children"),
        Output(component_id="selected_nm_title", component_property="children"),
        Output(component_id="selected_nm_loader", component_property="children"),
        Output(component_id={
            'type': 'infer_form_control',
            "name": "TargetResourceParameter",
            "index": ALL,
            "control_type": "basic"
        }, component_property='value'),
        Input(component_id='selected_nm', component_property='data'),
        State(component_id="stored_token", component_property="data")
    )
    def on_stored_selected_result_update_callback(nm, token):
        if nm is not None:
            content, title = build_selected_result(nm, token, app)
            id_to_fill = nm["id"]
            return content, title, no_update, [id_to_fill]

        return grey_box(), html.H5("Selected Neuron Morphology"), no_update, [None]

