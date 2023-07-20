from dataclasses import dataclass

from data.identifiable import Identifiable


@dataclass(init=True)
class Species(Identifiable):

    name: str

    @staticmethod
    def class_to_store(ct):
        return {"id": ct.id, "name": ct.name}

    @staticmethod
    def source_to_class(ct):
        return Species(id=ct["id"], name=ct["name"])

    @staticmethod
    def store_to_class(ct):
        return Species(id=ct["id"], name=ct["name"])