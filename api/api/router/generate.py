from urllib.parse import unquote
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import HTTPBearer
from starlette.requests import Request
from api.dependencies import retrieve_user
from api.exceptions import ResourceNotFoundException
from api.morpho_img import read_image

router = APIRouter()

require_bearer = HTTPBearer()


@router.get(
    "/morphology-image/{encoded_content_url}",
    dependencies=[Depends(require_bearer)],
    response_model=None,
    tags=["Morphology Image"],
)
def get_morphology_image(
    encoded_content_url: str,
    request: Request,
) -> Response:
    """
    Endpoint to get a preview image of a morphology
    """
    user = retrieve_user(request)
    authorization = f"Bearer {user.access_token}"

    content_url = unquote(encoded_content_url)

    try:
        image = read_image(authorization, content_url)

        return image
    except ResourceNotFoundException:
        raise HTTPException(
            status_code=404,
            detail=f"There was no distribution for that content url.",
        )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail=f"Something went wrong.",
        )
