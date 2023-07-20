from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from data.dict_key import DictKey


def on_filter_press(app):
    @app.callback(
        Output(component_id="stored_filters", component_property="data"),
        Input(component_id="filter_rules_button", component_property="n_clicks"),
        State(component_id="datatype_dropdown", component_property="value"),
        State(component_id="brain_region_dropdown", component_property="value"),
        State(component_id="cell_type_dropdown", component_property="value")
    )
    def on_filter_press_callback(n_clicks, data_types, brain_regions, cell_types):
        if n_clicks and n_clicks > 0:
            return {
                DictKey.BRAIN_REGIONS.value: brain_regions if brain_regions else [],
                DictKey.DATA_TYPES.value: data_types if data_types else [],
                DictKey.CELL_TYPES.value: cell_types if cell_types else []
                # DictKey.CONTRIBUTORS.value: contributors,
            }
        raise PreventUpdate
