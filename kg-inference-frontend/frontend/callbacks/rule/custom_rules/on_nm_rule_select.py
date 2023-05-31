from dash import Input, Output, State, no_update, ALL, html
from dash.exceptions import PreventUpdate

from data.result.result_resource import ResultResource
from layout.result.result_table import build_result_table
from layout.result.selected_result import build_selected_result
from layout.utils import grey_box, make_toast, ToastType
from query.forge import get_neuron_morphologies, get_neuron_morphology, ForgeError


def on_nm_rule_select(app):

    @app.callback(
        Output(component_id="stored_nm", component_property="data"),
        Output(component_id="nm_fetching_loader", component_property="children"),
        Input(component_id="stored_nm", component_property="clear_data"),
        State(component_id="stored_token", component_property="data"),
        State(component_id="sidebar_content", component_property="data")
    )
    def on_stored_nm_clear_data(cleared, token, sidebar_content):
        return get_neuron_morphologies(token, sidebar_content), no_update

    @app.callback(
        Output(component_id="nm_list", component_property="children"),
        Input(component_id="stored_nm", component_property="data")
    )
    def on_stored_nm_callback(stored_nm):
        if stored_nm is not None:
            return build_result_table(
                results=[ResultResource.store_to_class(e) for e in stored_nm.values()],
                table_id="datatable_nm", include_score=False, rule=None
            )
        raise PreventUpdate

    @app.callback(
        Output(component_id="selected_nm", component_property="data"),
        Output(component_id="toast_container_nm_fetch", component_property="children"),
        Input(component_id={
            "type": "infer_form_control",
            "name": "TargetResourceParameter",
            "index": ALL,
            "control_type": "basic"
        }, component_property="value"),
        State(component_id="stored_token", component_property="data"),
        State(component_id="sidebar_content", component_property="data"),
        prevent_initial_call=True
    )
    def on_nm_input_fill(selected_nm_input, token, sidebar_content):
        if selected_nm_input and selected_nm_input[0]:
            idx = selected_nm_input[0]
            try:
                nm = get_neuron_morphology(
                    nm_id=idx, token=token, sidebar_content=sidebar_content
                )
                return ResultResource.class_to_store(nm), no_update
            except ForgeError as e:
                return None, make_toast(ToastType.ERROR, str(e))

        raise PreventUpdate

    @app.callback(
        Output(component_id={
            "type": "infer_form_control",
            "name": "TargetResourceParameter",
            "index": ALL,
            "control_type": "basic"
        }, component_property="value"),
        Input(component_id="datatable_nm", component_property="selected_row_ids"),
    )
    def on_result_row_select_callback(selected_row_ids):
        if selected_row_ids and selected_row_ids[0]:
            idx = selected_row_ids[0]
            return [idx]
        return [None]

    @app.callback(
        Output(component_id="selected_nm_view", component_property="children"),
        Output(component_id="selected_nm_title", component_property="children"),
        Output(component_id="selected_nm_loader", component_property="children"),
        Input(component_id="selected_nm", component_property="data"),
        State(component_id="stored_token", component_property="data")
    )
    def on_stored_selected_result_update_callback(nm, token):
        if nm is not None:
            content, title = build_selected_result(nm, token, app)
            return content, title, no_update

        return grey_box(), html.H5("Selected Neuron Morphology"), no_update
