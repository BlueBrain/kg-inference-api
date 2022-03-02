import os

BBP_NEXUS_ENDPOINT = os.environ.get("BBP_NEXUS_ENDPOINT")
BBP_USERINFO_AUTH_ENDPOINT = f"https://bbpauth.epfl.ch/auth/realms/BBP/protocol/openid-connect/userinfo"
RULES_BUCKET = os.environ.get("RULES_BUCKET")

if os.environ.get("ENVIRONMENT") == "LOCAL":
    DEBUG_MODE = True
elif os.environ.get("ENVIRONMENT") == "DEV":
    DEBUG_MODE = True
else:
    DEBUG_MODE = False
