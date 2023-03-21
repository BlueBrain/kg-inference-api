import os


def get_env_vars():

    environment_variables = {
        "API_BASE": "https://kg-inference-api.kcpdev.bbp.epfl.ch",
        "NEXUS_ENDPOINT": "https://bbp.epfl.ch/nexus/v1",
        "NEXUS_CONFIG_PATH": "./frontend/config/forge-config.yaml"
    }

    environment_variables = dict(
        (key, os.environ.get(key, default=default))
        for key, default in environment_variables.items()
    )

    # print("\n".join([f"{key}: {value}" for key, value in environment_variables.items()]))

    for key, value in environment_variables.items():
        if value is None:
            raise Exception(f"Missing environment variable {key}")

    return environment_variables.values()


API_BASE, NEXUS_ENDPOINT, NEXUS_CONFIG_PATH = get_env_vars()
