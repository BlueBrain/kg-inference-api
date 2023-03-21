from dataclasses import dataclass
from data.utils import get_id


@dataclass(init=True)
class Contribution:
    label: str
    id: str

    def set_label(self, label):
        self.label = label
        return self

    @staticmethod
    def source_to_class(contribution_dict):
        contribution_dict = contribution_dict.get("agent", None)
        if not contribution_dict:
            return None
        return Contribution(id=get_id(contribution_dict), label=contribution_dict.get("label", None))

    @staticmethod
    def class_to_store(contribution):
        return {"agent": {"id": contribution.id, "label": contribution.label}}
