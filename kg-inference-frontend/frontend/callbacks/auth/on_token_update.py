from dash import Input, Output, no_update
from dash.exceptions import PreventUpdate

from layout.utils import make_toast, ToastType
from query.forge import get_cell_types, get_data_types, get_brain_regions, ForgeError, \
    get_forge_neuroscience_datamodels, get_m_types, get_e_types, get_entities, get_species
from data.dict_key import DictKey, dict_key_class_map


def on_token_update(app):
    @app.callback(
        Output(component_id="toast_container_sidebar_fetch", component_property='children'),
        Output(component_id="sidebar_content", component_property="data"),
        Output(component_id="sidebar_fetching_loader", component_property="children"),
        Input(component_id='stored_token', component_property='data'),
    )
    def on_token_update_callback(token):
        if token is not None:
            try:
                forge = get_forge_neuroscience_datamodels(token)

                dict_key_data_map = {
                    DictKey.BRAIN_REGIONS: get_brain_regions(forge),
                    DictKey.CELL_TYPES: get_cell_types(forge),
                    DictKey.DATA_TYPES: get_data_types(forge),
                    DictKey.M_TYPES: get_m_types(forge),
                    DictKey.E_TYPES: get_e_types(forge),
                    DictKey.SPECIES: get_species(forge),
                    # DictKey.CONTRIBUTORS: get_contributors(forge)
                    # DictKey.ENTITIES: get_entities(forge)
                }

                sidebar_content = dict(
                    (
                        dict_key.value,
                        [
                         dict_key_class_map[dict_key].class_to_store(e)
                         for e in dict_key_data_map[dict_key]
                        ]
                     )
                    for dict_key in DictKey if dict_key not in
                    [DictKey.CONTRIBUTORS, DictKey.ENTITIES])

                return (
                    make_toast(ToastType.INFORMATION, "Loaded sidebar information"),
                    sidebar_content,
                    no_update
                )
            except ForgeError as e:
                return (
                    make_toast(ToastType.ERROR, str(e)),
                    no_update,
                    no_update
                )
        raise PreventUpdate
