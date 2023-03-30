from dash import Input, Output, no_update
from dash.exceptions import PreventUpdate
from layout.sidebar.sidebar import build_sidebar
from data.dict_key import DictKey, dict_key_class_map
from data.data_type import DataType
from data.brain_region import BrainRegion
from data.cell_type import CellType


def on_stored_sidebar_content_update(app):
    @app.callback(
        Output(component_id="sidebar", component_property='children'),
        Output(component_id="sidebar_building_loader", component_property="children"),
        Input(component_id="sidebar_content", component_property="data"),
    )
    def on_sidebar_content_update_callback(sidebar_content):
        if sidebar_content is not None:

            def sidebar_content_to_class(dict_key: DictKey):
                return [
                    dict_key_class_map[dict_key].store_to_class(el)
                    for el in sidebar_content[dict_key.value]
                ]

            return (
                build_sidebar(
                    brain_regions=sidebar_content_to_class(DictKey.BRAIN_REGIONS),
                    data_types=sidebar_content_to_class(DictKey.DATA_TYPES),
                    cell_types=sidebar_content_to_class(DictKey.CELL_TYPES),
                    contributors=None
                ),
                no_update
            )

        raise PreventUpdate
