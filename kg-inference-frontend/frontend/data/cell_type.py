from dataclasses import dataclass


@dataclass(init=True)
class CellType:
    name: str
    id: str

    @staticmethod
    def class_to_store(ct):
        return {"id": ct.id, "name": ct.name}

    @staticmethod
    def source_to_class(ct):
        return CellType(id=ct["id"], name=ct["name"])

    @staticmethod
    def store_to_class(ct):
        return CellType(id=ct["id"], name=ct["name"])


class MType(CellType):
    ...
