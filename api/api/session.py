from kgforge.core import KnowledgeGraphForge
from api import config


class UserSession:

    def __init__(self, token: str) -> None:
        self.endpoint = config.BBP_NEXUS_ENDPOINT
        # adds the rules bucket
        self.forges = {
            config.RULES_BUCKET: KnowledgeGraphForge(
                "./api/config/forge-config.yaml",
                endpoint=self.endpoint,
                bucket=config.RULES_BUCKET,
                token=token,
                debug=config.DEBUG_MODE),
            config.DATAMODELS_BUCKET: KnowledgeGraphForge(
                "./api/config/forge-config_datamodels.yaml",
                endpoint=self.endpoint,
                bucket=config.DATAMODELS_BUCKET,
                token=token,
                debug=config.DEBUG_MODE),
        }
        self.token = token

    def get_rules_forge(self):
        """
        Returns the forge object that includes the rules

        :return:
        """
        return self.forges[config.RULES_BUCKET]

    def get_datamodels_forge(self):
        """
        Returns the forge object that includes the datamodels

        :return:
        """
        return self.forges[config.DATAMODELS_BUCKET]

    def get_or_create_forge_session(self, org: str, project: str) -> KnowledgeGraphForge:
        """
        Retrieves or creates a forge session for the given organization and project.
        Then returns the forge object

        :param org:
        :param project:
        :return:
        """
        bucket = f"{org}/{project}"

        # if the bucket does not exist in the session
        if bucket not in self.forges:
            session = KnowledgeGraphForge(
                "./api/config/forge-config.yaml",
                endpoint=self.endpoint,
                token=self.token,
                bucket=bucket)
            self.forges[bucket] = session
        # if the token stored in the forge is different than the one of the session
        elif self.forges[bucket]._store.token != self.token:
            self.forges[bucket] = KnowledgeGraphForge(
                "./api/config/forge-config.yaml",
                endpoint=self.endpoint,
                token=self.token,
                bucket=bucket)
        return self.forges[bucket]

    def re_initialize_token(self, new_token: str) -> None:
        """
        Re-initializes the session token and the rules bucket

        :param new_token: the new token to re-initialize the values
        :return:
        """
        self.token = new_token
        self.forges[config.RULES_BUCKET] = KnowledgeGraphForge(
            "./api/config/forge-config.yaml",
            endpoint=self.endpoint,
            bucket=config.RULES_BUCKET,
            token=new_token,
            debug=config.DEBUG_MODE)
        self.forges[config.DATAMODELS_BUCKET] = KnowledgeGraphForge(
            "./api/config/forge-config.yaml",
            endpoint=self.endpoint,
            bucket=config.DATAMODELS_BUCKET,
            token=new_token,
            debug=config.DEBUG_MODE)

    def forge_is_valid(self, access_token: str) -> bool:
        """
        Checks if the existing forge object is still valid by checking
        if the received access token is the same as the one stored in the forge object

        :param access_token: the received access token
        :return: True if it is valid, False otherwise
        """
        return self.token == access_token
