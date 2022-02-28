from api import config
from kgforge.core import KnowledgeGraphForge


class UserForgeSession:

    def __init__(self, bucket: str, access_token: str) -> None:
        self.endpoint = config.BBP_NEXUS_ENDPOINT
        self.bucket = bucket
        self.forge = self.initialize_forge_object(access_token=access_token)

    def initialize_forge_object(self, access_token: str) -> KnowledgeGraphForge:
        """
        Initializes and returns a forge object

        :param access_token:
        :return:
        """
        return KnowledgeGraphForge(
            "./api/config/forge-config.yaml",
            endpoint=self.endpoint,
            bucket=self.bucket,
            token=access_token,
            debug=True)

    def forge_is_valid(self, access_token: str) -> bool:
        """
        Checks if the existing forge object is still valid by checking if the received access token is the same as
        the one stored in the forge object

        :param access_token: the received access token
        :return: True if it is valid, False otherwise
        """
        return self.forge._store.token == access_token
