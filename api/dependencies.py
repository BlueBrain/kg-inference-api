import requests
from fastapi import HTTPException
from starlette.requests import Request
from api import config
from api.user import User


async def require_user_auth(request: Request) -> dict:
    """
    Dependency function to require credentials on a request.

    Checks if token is provided and returns the token if it is and 401 otherwise

    :param request:
    :return:
    """
    access_token = request.headers.get("authorization")
    if access_token is None:
        raise HTTPException(status_code=401, detail="Credentials not provided")
    else:
        user = requests.get(config.BBP_USERINFO_AUTH_ENDPOINT, headers={"Authorization": access_token}).json()
        if "error" in user and user["error"] == "invalid_token":
            raise HTTPException(status_code=401,
                                detail="Token verification failed. Check if the token is still valid or expired")
        else:
            return {
                "user": User(username=user.get("preferred_username")),
                "access_token": access_token.replace("Bearer ", "")
            }


async def require_nexus_project(organization: str, project: str) -> str:
    """
    Dependency function to require a nexus project as parameter

    :param organization: a Nexus organization
    :param project: a Nexus project
    :return: the bucket
    """
    return f"{organization}/{project}"
