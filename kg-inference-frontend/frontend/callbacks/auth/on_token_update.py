from dash import Input, Output, no_update
from dash.exceptions import PreventUpdate

from data.entity import Entity
from layout.utils import make_toast, ToastType
from query.forge import get_cell_types, get_data_types, get_brain_regions, ForgeError, \
    get_forge_neuroscience_datamodels, get_m_types, get_e_types, get_entities, get_species
from data.brain_region import BrainRegion
from data.data_type import DataType
from data.cell_type import CellType, MType, EType
from data.dict_key import DictKey
from data.species import Species


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
                brain_regions = get_brain_regions(forge)
                data_types = get_data_types(forge)
                cell_types = get_cell_types(forge)
                m_types = get_m_types(forge)
                e_types = get_e_types(forge)
                species = get_species(forge)
                # entities = get_entities(forge)
                # contributors = get_contributors(forge)

                return (
                    make_toast(ToastType.INFORMATION, "Loaded sidebar information"),
                    {
                        DictKey.BRAIN_REGIONS.value: [BrainRegion.class_to_store(br) for br in brain_regions],
                        DictKey.DATA_TYPES.value: [DataType.class_to_store(dt) for dt in data_types],
                        DictKey.CELL_TYPES.value: [CellType.class_to_store(c) for c in cell_types],
                        DictKey.M_TYPES.value: [MType.class_to_store(c) for c in m_types],
                        DictKey.E_TYPES.value: [EType.class_to_store(c) for c in e_types],
                        DictKey.SPECIES.value: [Species.class_to_store(s) for s in species]
                        # DictKey.ENTITIES.value: [Entity.class_to_store(e) for e in entities]
                    },
                    no_update
                )
            except ForgeError as e:
                return (
                    make_toast(ToastType.ERROR, str(e)),
                    no_update,
                    no_update
                )
        raise PreventUpdate
