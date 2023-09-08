from kgforge.core import KnowledgeGraphForge
from api import config
import os
import yaml


class UserSession:
    default_config_path = "./config/forge-config.yaml"

    def _build_forge(self, bucket: str, es_view: str = None, sparql_view: str = None) -> \
            KnowledgeGraphForge:
        """
        Creates a KnowledgeGraphForge instance from a bucket name
        :param bucket: the bucket the instance will be tied to
        :return: a KnowledgeGraphForge instance
        """
        config_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            UserSession.default_config_path
        )

        with open(config_path) as e:
            conf = yaml.safe_load(e)
            if bucket == "neurosciencegraph/datamodels":
                conf["Model"]["context"]["iri"] = 'https://neuroshapes.org'

        args = dict(
            configuration=conf,
            endpoint=config.BBP_NEXUS_ENDPOINT,
            bucket=bucket,
            token=self.token,
            debug=config.DEBUG_MODE
        )

        search_endpoints = {}

        if es_view is not None:
             search_endpoints["elastic"] = {"endpoint": es_view}

        if sparql_view is not None:
            search_endpoints["sparql"] = {"endpoint": sparql_view}

        if len(search_endpoints) > 0:
            args["searchendpoints"] = search_endpoints

        return KnowledgeGraphForge(**args)

    def __init__(self, token: str) -> None:
        self.re_initialize_token(token)

    def get_rules_forge(self) -> KnowledgeGraphForge:
        """
        Returns the forge object that includes the rules

        :return:
        """
        return self.forges[config.RULES_BUCKET]

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
        # if the token stored in the forge is different from the one of the session
        if bucket not in self.forges or self.forges[bucket]._store.token != self.token:
            self.forges[bucket] = self._build_forge(bucket=bucket)

        return self.forges[bucket]

    def re_initialize_token(self, new_token: str) -> None:
        """
        Re-initializes the session token and the rules bucket

        :param new_token: the new token to re-initialize the values
        :return:
        """
        self.token = new_token

        self.forges = {
            config.RULES_BUCKET: self._build_forge(
                bucket=config.RULES_BUCKET, es_view=config.ES_RULE_VIEW,
                sparql_view=config.SPARQL_RULE_VIEW
            )
        }

    def forge_is_valid(self, access_token: str) -> bool:
        """
        Checks if the existing forge object is still valid by checking
        if the received access token is the same as the one stored in the forge object

        :param access_token: the received access token
        :return: True if it is valid, False otherwise
        """
        return self.token == access_token
