from dataclasses import dataclass


@dataclass(init=True)
class DataType:

    name: str
    id: str

    @staticmethod
    def class_to_store(c):
        return {"id": c.id, "name": c.name}

    @staticmethod
    def source_to_class(c):
        return DataType(id=c["id"], name=c["name"])

    @staticmethod
    def store_to_class(c):
        return DataType(id=c["id"], name=c["name"])
