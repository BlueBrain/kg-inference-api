from dash import Input, Output, no_update
from dash.exceptions import PreventUpdate
from layout.utils import make_toast, ToastType
from layout.sidebar.sidebar import build_sidebar
from data.dict_key import DictKey
from data.data_type import DataType
from data.brain_region import BrainRegion
from data.cell_type import CellType


def on_stored_sidebar_content_update(app):
    @app.callback(
        Output(component_id="toast_container_sidebar_build", component_property='children'),
        Output(component_id="sidebar", component_property='children'),
        Output(component_id="sidebar_building_loader", component_property="children"),
        Input(component_id="sidebar_content", component_property="data"),
    )
    def on_sidebar_content_update_callback(sidebar_content):
        if sidebar_content is not None:

            brain_regions = [BrainRegion.store_to_class(el) for el in sidebar_content[DictKey.BRAIN_REGIONS.value]]
            data_types = [DataType.store_to_class(el) for el in sidebar_content[DictKey.DATA_TYPES.value]]
            cell_types = [CellType.store_to_class(el) for el in sidebar_content[DictKey.CELL_TYPES.value]]

            # contributors = get_contributors(token)

            return (
                make_toast(ToastType.INFORMATION, "Built sidebar"),
                build_sidebar(
                    brain_regions=brain_regions,
                    data_types=data_types,
                    cell_types=cell_types,
                    contributors=None
                ),
                no_update
            )

        raise PreventUpdate
