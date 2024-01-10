"""
Module: generate.py

This module defines a FastAPI router for handling requests related to morphology images.
It includes an endpoint to get a preview image of a morphology.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from fastapi.security import HTTPBearer
from starlette.requests import Request
from api.dependencies import retrieve_user
from api.exceptions import InvalidUrlParameterException, ResourceNotFoundException
from api.morpho_img import read_image

router = APIRouter()

require_bearer = HTTPBearer()


@router.get(
    "/morphology-image",
    dependencies=[Depends(require_bearer)],
    response_model=None,
    tags=["Morphology Image"],
)
def get_morphology_image(
    content_url: str,
    request: Request,
    dpi: Optional[int] = Query(None, ge=10, le=600),
) -> Response:
    """
    Endpoint to get a preview image of a morphology
    """
    user = retrieve_user(request)
    authorization = f"Bearer {user.access_token}"

    try:
        image = read_image(authorization, content_url, dpi)

        return image
    except InvalidUrlParameterException as exc:
        raise HTTPException(
            status_code=422,
            detail="Invalid content_url parameter in request.",
        ) from exc
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
