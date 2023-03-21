from dataclasses import dataclass


@dataclass(init=True)
class Distribution:
    encoding_format: str
    at_location: str
    content_url: str

    @staticmethod
    def source_to_class(distribution_dict):
        cu = distribution_dict.get("contentUrl", None)
        al = distribution_dict.get("atLocation", None)
        if al is not None:
            al = al.get("location", None)
        ef = distribution_dict.get("encodingFormat", None)
        return Distribution(at_location=al, encoding_format=ef, content_url=cu)
