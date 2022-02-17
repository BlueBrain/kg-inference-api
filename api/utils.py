from kgforge.core import KnowledgeGraphForge
from starlette.requests import Request
from api.session import UserForgeSession


def get_or_create_forge_session(request: Request, username, access_token: str = "") -> KnowledgeGraphForge:
    """
    Returns an existing forge session or creates and returns a new one

    If the session already exists, checks if the forge object is still valid. If it is not, then initializes a new
    forge object

    :param request:
    :param username:
    :param bucket:
    :param access_token:
    :return:
    """
    # if a session does not exist with this user
    if username not in request.session:
        session = UserForgeSession(bucket="dke/inference-test", access_token=access_token)
        request.session[username] = session
        return session.forge
    else:
        session = request.session[username]
        # if the forge object in the session is not still valid, initializes a new one
        if not session.forge_is_valid(access_token=access_token):
            session.forge = session.initialize_forge_object(access_token=access_token)
        return session.forge
