from abc import abstractmethod
from dataclasses import dataclass


@dataclass(init=True)
class Identifiable:
    id: str

    @staticmethod
    @abstractmethod
    def class_to_store(el):
        pass

    @staticmethod
    @abstractmethod
    def source_to_class(el):
        pass

    @staticmethod
    @abstractmethod
    def store_to_class(el):
        pass
