from dataclasses import dataclass
from kgforge.core.wrappings.dict import DictWrapper
from data.utils import get_id


@dataclass(init=True)
class Image:
    stimulus_type: DictWrapper
    repetition: str
    id: str
    about: str

    @staticmethod
    def source_to_class(image_dict):
        stimulus_type = DictWrapper(image_dict.get("stimulusType", {}))
        repetition = image_dict.get("repetition", None)
        about = image_dict.get("about", None)
        id_ = get_id(image_dict)
        return Image(stimulus_type=stimulus_type, repetition=repetition, id=id_, about=about)

    @staticmethod
    def class_to_store(image):
        return {"id": image.id, "about": image.about, "stimulusType": image.stimulus_type,
                "repetition": image.repetition}

    def set_stimulus_type(self, st):
        self.stimulus_type = st
        return self
