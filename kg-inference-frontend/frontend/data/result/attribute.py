from enum import Enum


class ExtendedEnum(Enum):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class Attribute(ExtendedEnum):
    SCORE = "Combined Score"
    SCORE_BREAKDOWN = "Score breakdown"
    IMAGE_STIMULUS_TYPE_LABEL = "Image Stimulus Type Label"
    ORG = "Org"
    PROJECT = "Project"
    ID = "id"
    NAME = "Name"
    SUBJECT = "Subject"
    SUBJECT_ID = "Subject Id"
    TYPE = "Type"
    BRAIN_REGION = "Brain Region"
    BRAIN_REGION_ID = "Brain Region Id"
    CONTRIBUTION = "Contribution"
    CONTRIBUTION_LABEL = "Contributor"
    # CLASSIFICATION = "Classification"
    LINK = "Nexus Fusion Link"
    ENCODING_FORMAT = "Encoding Format"
    AT_LOCATION = "At Location"
    CONTENT_URL = "Content URL"
    E_TYPE = "E Type"
    M_TYPE = "M Type"
    IMAGE = "Image"
    DISTRIBUTION = "Distribution"
