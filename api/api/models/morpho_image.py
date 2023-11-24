from fastapi_camelcase import CamelModel


class MorphoImageBody(CamelModel):
    """The body of the morpho-image requests"""

    id: str
