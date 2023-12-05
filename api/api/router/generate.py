"""
Module: generate.py

This module defines a FastAPI router for handling requests related to morphology images.
It includes an endpoint to get a preview image of a morphology.
"""

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import HTTPBearer
from starlette.requests import Request
from api.dependencies import retrieve_user
from api.exceptions import ResourceNotFoundException
from api.morpho_img import read_image

router = APIRouter()

require_bearer = HTTPBearer()


@router.get(
    "/morphology-image/{content_url}",
    dependencies=[Depends(require_bearer)],
    response_model=None,
    tags=["Morphology Image"],
)
def get_morphology_image(
    content_url: str,
    request: Request,
) -> Response:
    """
    Endpoint to get a preview image of a morphology
    """
    user = retrieve_user(request)
    authorization = f"Bearer {user.access_token}"

    try:
        image = read_image(authorization, content_url)

        return image
    except ResourceNotFoundException as exc:
        raise HTTPException(
            status_code=404,
            detail="There was no distribution for that content url.",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail="Something went wrong.",
        ) from exc
