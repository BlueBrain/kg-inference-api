"""
Module: dependencies.py

This module provides functions related to user authentication using JWT tokens and handling user sessions.
"""

from fastapi import HTTPException
from starlette.requests import Request
import jwt
from api.session import UserSession
from api.user import User


def retrieve_user(request: Request) -> User:
    """
    Retrieves user from BBP auth endpoint. If token is invalid, throws 401 error

    :param request: FastAPI Request object.
    :return: User object containing username and access token.
    :raises HTTPException: Thrown with a 401 status code if the access token is invalid or has expired.
    """
    access_token = request.headers.get("authorization").replace("Bearer ", "")
    try:
        decoded = jwt.decode(access_token, options={"verify_signature": False})
        return User(
            username=decoded.get("preferred_username"), access_token=access_token
        )
    except jwt.ExpiredSignatureError as exp_signature_error:
        raise HTTPException(
            status_code=401, detail="Access token has expired"
        ) from exp_signature_error
    except jwt.InvalidTokenError as inv_token_error:
        raise HTTPException(
            status_code=401, detail="Access token is invalid"
        ) from inv_token_error


async def require_user_session(request: Request) -> UserSession:
    """
    Dependency function to require a forge session.

    Returns an existing forge session or creates and returns a new one

    If the session already exists, checks if the forge object is still valid. If it is not, then initializes a new
    forge object

    :param request: FastAPI Request object.
    :return: UserSession object representing the user's session.
    """
    user = retrieve_user(request)
    user_session = UserSession(token=user.access_token)
    return user_session
