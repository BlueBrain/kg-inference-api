from dataclasses import dataclass
from abc import ABC, abstractmethod
from jsonpath_rw import parse
from data.utils import to_string
from data.result.attribute import Attribute


@dataclass
class Result(ABC):

    def __init__(self, json_object):
        self.__dict__ = json_object

    @staticmethod
    @abstractmethod
    def source_to_class(c):  # Shouldn't be used anyway
        ...

    @staticmethod
    @abstractmethod
    def store_to_class(c):
        ...

    @staticmethod
    @abstractmethod
    def to_result_object(obj, forge):
        ...

    @abstractmethod
    def paths(self) -> dict:
        ...

    @abstractmethod
    def get_cell_type(self, is_e: bool):
        ...

    @abstractmethod
    def get_attribute(self, attr: Attribute):
        ...

    def get_path(self, attr: Attribute):
        return self.paths()[attr]

    def get_attributes(self, ignore_keys=None):
        if ignore_keys is None:
            ignore_keys = []
        return dict((attr.value, self.get_attribute(attr)) for attr in
                    list(Attribute) if attr not in ignore_keys)

    @staticmethod
    def get_value(obj, path, to_str):
        temp = [t.value for t in parse(path).find(obj) if t.value]

        if len(temp) == 0:
            return None

        return to_string(temp) if to_str else temp
