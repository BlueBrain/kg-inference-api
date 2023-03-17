import os

def get_env_vars():

    environment_variables = {
        "BBP_NEXUS_ENDPOINT": None,
        "ENVIRONMENT": None,
        "RULES_BUCKET": None,
        "DATAMODELS_BUCKET": None,
        "WHITELISTED_CORS_URLS": "",  # can be optional
        "NEXUS_TOKEN": "", # can be optional
        "BBP_USERINFO_AUTH_ENDPOINT": "https://bbpauth.epfl.ch/auth/realms/BBP/protocol/openid-connect/userinfo"
    }

    environment_variables = dict(
        (key, os.environ.get(key, default=default))
        for key, default in environment_variables.items()
    )

    environment_variables["DEBUG_MODE"] = \
        environment_variables["ENVIRONMENT"] == "LOCAL" or environment_variables["DEBUG_MODE"] == "DEV"

    for key, value in environment_variables.items():
        if value is None:
            raise Exception(f"Missing environment variable {key}")

    return environment_variables.values()


BBP_NEXUS_ENDPOINT, ENVIRONMENT, RULES_BUCKET, DATAMODELS_BUCKET, WHITELISTED_CORS_URLS, NEXUS_TOKEN, \
    BBP_USERINFO_AUTH_ENDPOINT, DEBUG_MODE = get_env_vars()
