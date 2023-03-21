from data.result.contribution import Contribution
from data.result.result import Result
from data.result.attribute import Attribute
from data.utils import enforce_list, get_type, to_string, get_id
from data.result.distribution import Distribution
from data.result.image import Image


class ResultResource(Result):

    @staticmethod
    def to_result_object(element, forge):
        new_obj = forge.as_json(element)
        nexus_link = element._store_metadata._self
        org, project = element._store_metadata._project.split("/")[-2:]

        new_obj["org"] = org
        new_obj["project"] = project
        new_obj["nexus_link"] = nexus_link

        resource = ResultResource(json_object=new_obj)

        if "image" in new_obj and "stimulus" in new_obj:
            def get_stimulus_in_resource_by_id(st_id, res):
                return next(
                    obj["stimulusType"]
                    for obj in res["stimulus"]
                    if obj["stimulusType"]["id"] == st_id
                )

            resource.set_images([
                image.set_stimulus_type(get_stimulus_in_resource_by_id(image.stimulus_type.id, new_obj))
                for image in resource.get_image()
                if image.stimulus_type and "label" not in image.stimulus_type
            ])

        return resource

    @staticmethod
    def source_to_class(c):
        return ResultResource(json_object=c)

    @staticmethod
    def store_to_class(c):
        return ResultResource(json_object=c)

    @staticmethod
    def class_to_store(c):
        return c.__dict__

    def paths(self):
        return {
            Attribute.ID: "id",
            Attribute.NAME: "$[label, name]",
            Attribute.SUBJECT: "subject.species.label",
            Attribute.SUBJECT_ID: "subject.species.id",
            Attribute.TYPE: "type",
            Attribute.BRAIN_REGION: "brainLocation.[brainRegion, layer].label",
            Attribute.BRAIN_REGION_ID: "brainLocation.[brainRegion, layer].id",
            Attribute.CONTRIBUTION_LABEL: "contribution[*].agent.label",
            Attribute.IMAGE_STIMULUS_TYPE_LABEL: "image[*].stimulusType.label",
            Attribute.ENCODING_FORMAT: "distribution[*].encodingFormat",
            Attribute.AT_LOCATION: "distribution[*].atLocation.location",
            Attribute.CONTENT_URL: "distribution[*].contentUrl",
            Attribute.IMAGE: "image[*]",
            Attribute.LINK: "nexus_link",
            Attribute.ORG: "org",
            Attribute.PROJECT: "project"
            # Attribute.CONTRIBUTION_ID: "contribution[*].agent.id",
            # Attribute.E_TYPE: "annotation[*]['hasBody'][?(@.type contains 'EType')].label",
            # Attribute.M_TYPE: "annotation[*]['hasBody'][?(@.type contains 'MType')].label"
            # "Object of Study": ["objectOfStudy.label", "objectOfStudy.id"],
            # "License": ["license[*].label", "license[*].id"],
        }

    def get_attribute(self, attr: Attribute, to_str=True):
        if attr == Attribute.ID:
            return get_id(self.__dict__)
        if attr == Attribute.IMAGE:
            return self.get_image()  # cannot be str
        if attr == Attribute.E_TYPE:
            return self.get_cell_type(is_e=True)
        if attr == Attribute.M_TYPE:
            return self.get_cell_type(is_e=False)
        if attr == Attribute.IMAGE:
            return self.get_image()  # cannot be str
        if attr == Attribute.DISTRIBUTION:
            return self.get_distribution()  # cannot be str
        if attr == Attribute.TYPE:
            return get_type(self.__dict__) if not to_str else to_string(get_type(self.__dict__))
        if attr == Attribute.CONTRIBUTION:
            return self.get_contribution()
            # Can't json path with @ in field

        return Result.get_value(self.__dict__, self.get_path(attr), to_str=to_str)

    def get_contribution(self):
        contributions = self.__dict__.get("contribution", None)

        if not contributions:
            return []

        return [Contribution.source_to_class(c) for c in enforce_list(contributions)]

    def set_contributions(self, contributions: [Contribution]):
        self.__dict__["contribution"] = [Contribution.class_to_store(c) for c in contributions]
        return self

    def set_images(self, images: [Image]):
        self.__dict__["image"] = [Image.class_to_store(i) for i in images]
        return self

    def get_distribution(self):

        distributions = self.__dict__.get("distribution", None)

        if not distributions:
            return []

        return [Distribution.source_to_class(e) for e in enforce_list(distributions)]

    def get_image(self):

        images = self.__dict__.get("image", None)

        if not images:
            return []

        return [Image.source_to_class(e) for e in enforce_list(images)]

    def get_cell_type(self, is_e):

        annotation = self.__dict__.get("annotation", None)

        if not annotation:
            return None

        type_str = "EType" if is_e else "MType"
        for obj in enforce_list(annotation):
            for body_el in enforce_list(obj["hasBody"]):
                if type_str in get_type(body_el):
                    return body_el["label"]
        return None
