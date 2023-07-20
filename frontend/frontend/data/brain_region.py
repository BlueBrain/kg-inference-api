from dataclasses import dataclass

from data.identifiable import Identifiable


@dataclass(init=True)
class BrainRegion(Identifiable):

    name: str
    hasPart: any
    isPart: any

    @staticmethod
    def class_to_store(br):
        return {
            "id": br.id,
            "name": br.name,
            "hasPart": br.hasPart,
            "isPart": br.isPart
        }

    @staticmethod
    def source_to_class(br):
        return BrainRegion(
            id=br["id"],
            name=str(br["name"]),
            hasPart=br.get("hasPart", None),
            isPart=br.get("isPart", None)
        )

    @staticmethod
    def store_to_class(br):
        return BrainRegion(
            id=br["id"],
            name=br["name"],
            hasPart=br["hasPart"],
            isPart=br["isPart"]
        )
