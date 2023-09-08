import os


def get_env_vars():
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
        (key, os.environ.get(key, default=default))
        for key, default in environment_variables.items()
    )

    environment_variables["DEBUG_MODE"] = \
        environment_variables["ENVIRONMENT"] == "LOCAL" \
        or environment_variables["ENVIRONMENT"] == "DEV"

    for key, value in environment_variables.items():
        if value is None:
            raise Exception(f"Missing environment variable {key}")

    return environment_variables.values()


BBP_NEXUS_ENDPOINT, ENVIRONMENT, RULES_BUCKET, ES_RULE_VIEW, SPARQL_RULE_VIEW, \
    WHITELISTED_CORS_URLS, NEXUS_TOKEN, DEBUG_MODE = get_env_vars()
