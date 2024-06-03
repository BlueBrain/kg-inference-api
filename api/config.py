"""
Module: config

This module provides a utility for configuring environment variables used in a specific application.

Usage:
    The module can be imported and used to configure environment variables for the application.
    Example:
        from environment_configurator import BBP_NEXUS_ENDPOINT, ENVIRONMENT, RULES_BUCKET, ...
        # Use the configured variables in your application logic.
"""

import os
from dotenv import load_dotenv


load_dotenv()


def get_env_vars():
    """
    Retrieves and configures required environment variables for the application.

    Returns:
        tuple: A tuple containing the configured values for BBP_NEXUS_ENDPOINT, ENVIRONMENT,
               RULES_BUCKET, ES_RULE_VIEW, SPARQL_RULE_VIEW, WHITELISTED_CORS_URLS,
               NEXUS_TOKEN, and DEBUG_MODE.
    Raises:
        Exception: If any of the required environment variables is missing.
    """
    environment_variables = {
        "BBP_NEXUS_ENDPOINT": None,
        "ENVIRONMENT": None,
        "RULES_BUCKET": None,
        "ES_RULE_VIEW": None,
        "SPARQL_RULE_VIEW": None,
        "WHITELISTED_CORS_URLS": "",  # can be optional
        "NEXUS_TOKEN": "",  # can be optional
    }

    environment_variables = dict(
        (key, os.environ.get(key, default=default)) for key, default in environment_variables.items()
    )

    environment_variables["DEBUG_MODE"] = (
        environment_variables["ENVIRONMENT"] == "LOCAL" or environment_variables["ENVIRONMENT"] == "DEV"
    )

    for key, value in environment_variables.items():
        if value is None:
            raise RuntimeError(f"Missing environment variable {key}")

    return environment_variables.values()


(
    BBP_NEXUS_ENDPOINT,
    ENVIRONMENT,
    RULES_BUCKET,
    ES_RULE_VIEW,
    SPARQL_RULE_VIEW,
    WHITELISTED_CORS_URLS,
    NEXUS_TOKEN,
    DEBUG_MODE,
) = get_env_vars()
