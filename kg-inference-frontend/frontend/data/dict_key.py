from enum import Enum
from data.brain_region import BrainRegion
from data.cell_type import CellType, MType, EType
from data.data_type import DataType
from data.result.attribute import Attribute
from data.species import Species


class DictKey(Enum):
    BRAIN_REGIONS = "brain_regions"
    CELL_TYPES = "cell_types"
    DATA_TYPES = "data_types"
    CONTRIBUTORS = "contributors"
    M_TYPES = "m_types"
    E_TYPES = "e_types"
    SPECIES = "species"
    ENTITIES = "entities"


dict_key_class_map = {
    DictKey.BRAIN_REGIONS: BrainRegion,
    DictKey.CELL_TYPES: CellType,
    DictKey.DATA_TYPES: DataType,
    # DictKey.CONTRIBUTORS: ,
    # DictKey.ENTITIES: ,
    DictKey.M_TYPES: MType,
    DictKey.E_TYPES: EType,
    DictKey.SPECIES: Species
}

dict_key_attribute_map = {
    DictKey.BRAIN_REGIONS: Attribute.BRAIN_REGION,
    DictKey.DATA_TYPES: Attribute.TYPE,
    DictKey.M_TYPES: Attribute.M_TYPE,
    DictKey.E_TYPES: Attribute.E_TYPE,
    DictKey.SPECIES: Attribute.SPECIES
    # DictKey.CONTRIBUTORS: ,
    # DictKey.ENTITIES: ,
    # DictKey.CELL_TYPES: ,
}