from fastapi import HTTPException
from starlette.requests import Request
import jwt
from api.session import UserSession
from api.user import User


def retrieve_user(request: Request) -> User:
    """
    Retrieves user from BBP auth endpoint. If token is invalid, throws 401 error

    :param request:
    :return:
    """
    access_token = request.headers.get("authorization").replace("Bearer ", "")
    try:
        decoded = jwt.decode(
            access_token, options={"verify_signature": False}
        )
        return User(username=decoded.get("preferred_username"), access_token=access_token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Access token is invalid")


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
    user_session = UserSession(token=user.access_token)
    return user_session
