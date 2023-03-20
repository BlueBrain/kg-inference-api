from data.result.attribute import Attribute
from data.result.result import Result


class ResultSparql(Result):

    @staticmethod
    def source_to_class(c):
        pass

    @staticmethod
    def store_to_class(c):
        pass

    def get_cell_type(self, is_e: bool):
        pass

    def get_attribute(self, attr: Attribute):
        pass

    @staticmethod
    def to_result_object(obj, forge):
        single_valued = ["name", "id", "_self", "_project"]

        def split(el):
            return el.split(";") if ";" in el else el

        def split_check(el, key):
            return split(el) if key not in single_valued else el

        obj = dict((key, split_check(obj[key], key)) for key, value in obj.items())  # split values by separator

        keys_to_symbol = ["type", "classification_type"]

        def to_symbol(uri):
            return forge._model.context().to_symbol(uri)

        def to_symbol_check(el, key):
            return [to_symbol(val) for val in el] \
            if key not in single_valued and key in keys_to_symbol else el

        obj = dict((key, to_symbol_check(value, key)) for key, value in obj.items())

        org, project = obj["_project"].split("/")[-2:]
        obj["org"] = org
        obj["project"] = project
        obj["nexus_link"] = obj["_self"]
        return ResultSparql(json_object=obj)

    def paths(self):
        return {
            "id": "id",
            "Name": "name",
            "Subject": "subject",
            "Type": "type",
            "Brain Region": "brain_region",
            "Contribution": ["contribution_name", "contribution"],
            "Classification": ["classification_label", "classification_type"],
            "Nexus Fusion Link": "nexus_link",
            "Encoding Format": "distribution_encoding_format",
            "At Location": "distribution_at_location",
            "Content URL": "distribution_content_url"
        }
