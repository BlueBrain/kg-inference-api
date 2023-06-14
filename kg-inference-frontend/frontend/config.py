import os


def get_env_vars():
    environment_variables = {
        "ENVIRONMENT": "LOCAL",
        "NEXUS_ENDPOINT": "https://bbp.epfl.ch/nexus/v1",
        "NEXUS_CONFIG_PATH": os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                          "./config/forge-config.yaml"),
        "NEXUS_CONFIG_PATH_DATAMODELS": os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                     "./config/forge-config-datamodels.yaml"),
        "API_BASE": None
    }

    environment_variables = dict(
        (key, os.environ.get(key, default=default))
        for key, default in environment_variables.items()
    )

    env_to_api = {
        "LOCAL": "http://api:8080",
        "DEV": "https://kg-inference-api.kcpdev.bbp.epfl.ch",
        "PROD": "https://kg-inference-api.kcp.bbp.epfl.ch"
    }

    if environment_variables["API_BASE"] is None and \
            environment_variables["ENVIRONMENT"] is not None:
        environment_variables["API_BASE"] = env_to_api.get(
            environment_variables["ENVIRONMENT"], None)

    # print("\n".join([f"{key}: {value}" for key, value in environment_variables.items()]))

    for key, value in environment_variables.items():
        if value is None:
            raise Exception(f"Missing environment variable {key}")

    return environment_variables.values()


ENVIRONMENT, NEXUS_ENDPOINT, NEXUS_CONFIG_PATH, NEXUS_CONFIG_PATH_DATAMODELS, API_BASE = \
    get_env_vars()
