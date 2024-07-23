"""
Module: session.py

This module defines the UserSession class that manages KnowledgeGraphForge instances for user sessions.
"""

import os
from typing import Optional
import yaml
from kgforge.core import KnowledgeGraphForge
from api import config


def full_path(path):
    """
    Returns the absolute path by joining the current file's directory with the provided path.

    Parameters:
        - path (str): The relative path to be joined with the current file's directory.

    Returns:
        str: The absolute path.
    """
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), path)


class UserSession:
    """
    Manages KnowledgeGraphForge instances for user sessions.
    """

    default_config_path = "./config/forge-config.yaml"

    def _build_forge(self, bucket: str, es_view: str = None, sparql_view: str = None) -> KnowledgeGraphForge:
        """
        Creates a KnowledgeGraphForge instance from a bucket name
        :param bucket: the bucket the instance will be tied to
        :return: a KnowledgeGraphForge instance
        """
        config_path = full_path(UserSession.default_config_path)

        with open(config_path, encoding="utf-8") as e:
            conf = yaml.safe_load(e)

        conf["Store"]["file_resource_mapping"] = full_path(conf["Store"]["file_resource_mapping"])

        args = {
            "configuration": conf,
            "endpoint": config.BBP_NEXUS_ENDPOINT,
            "bucket": bucket,
            "token": self.token,
            "debug": config.DEBUG_MODE,
        }

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
        return self.forges[(config.RULES_BUCKET, config.ES_RULE_VIEW, config.SPARQL_RULE_VIEW)]

    def get_or_create_forge_session(
        self, org: str, project: str, es_view: Optional[str], sparql_view: Optional[str]
    ) -> KnowledgeGraphForge:
        """
        Retrieves or creates a forge session for the given organization and project.
        Then returns the forge object

        :param org:
        :param project:
        :param es_view:
        :param sparql_view:
        :return:
        """
        bucket = f"{org}/{project}"
        key = (bucket, es_view, sparql_view)
        # if the bucket does not exist in the session
        # if the token stored in the forge is different from the one of the session
        if key not in self.forges or not self.forge_is_valid(
            # pylint: disable=W0212
            self.forges[key]._store.token
        ):
            self.forges[key] = self._build_forge(bucket=bucket)

        return self._build_forge(bucket=bucket, es_view=es_view, sparql_view=sparql_view)

    def re_initialize_token(self, new_token: str) -> None:
        """
        Re-initializes the session token and the rules bucket

        :param new_token: the new token to re-initialize the values
        :return:
        """
        self.token = new_token

        self.forges = {
            (
                config.RULES_BUCKET,
                config.ES_RULE_VIEW,
                config.SPARQL_RULE_VIEW,
            ): self._build_forge(
                bucket=config.RULES_BUCKET,
                es_view=config.ES_RULE_VIEW,
                sparql_view=config.SPARQL_RULE_VIEW,
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
