import requests
from fastapi import HTTPException
from starlette.requests import Request
from api import config
from api.session import UserSession
from api.user import User


def retrieve_user(request: Request) -> User:
    """
    Retrieves user from BBP auth endpoint. If token is invalid, throws 401 error

    :param request:
    :return:
    """
    access_token = request.headers.get("authorization")
    user = requests.get(config.BBP_USERINFO_AUTH_ENDPOINT, headers={"Authorization": access_token}).json()
    if "error" in user and user["error"] == "invalid_token":
        raise HTTPException(status_code=401,
                            detail="Token verification failed. Check if the token is still valid or expired")
    else:
        return User(username=user.get("preferred_username"), access_token=access_token.replace("Bearer ", ""))


async def require_user_session(request: Request) -> UserSession:
    """
    Dependency function to require a forge session.

    Returns an existing forge session or creates and returns a new one

    If the session already exists, checks if the forge object is still valid. If it is not, then initializes a new
    forge object

    :param request:
    :return:
    """
    user = retrieve_user(request)
    # if a session does not exist with this user
    if user.username not in request.session:
        user_session = UserSession(token=user.access_token)
        request.session[user.username] = user_session
        return user_session
    else:
        user_session = request.session[user.username]
        # if the forge object in the session is not still valid, initializes a new one
        if not user_session.forge_is_valid(access_token=user.access_token):
            user_session.re_initialize_token(new_token=user.access_token)
        return user_session
