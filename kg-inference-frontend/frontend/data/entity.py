from dataclasses import dataclass

from data.identifiable import Identifiable


@dataclass(init=True)
class Entity(Identifiable):
    name: str

    @staticmethod
    def class_to_store(c):
        return {"id": c.id, "name": c.name}

    @staticmethod
    def source_to_class(c):
        return Entity(id=c["id"], name=c["name"])

    @staticmethod
    def store_to_class(c):
        return Entity(id=c["id"], name=c["name"])
