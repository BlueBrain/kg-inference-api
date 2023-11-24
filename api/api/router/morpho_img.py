import requests
import os.path

from typing import Union
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from fastapi.responses import FileResponse
from api.dependencies import require_user_session
from api.models.morpho_image import MorphoImageBody
from api.morpho_img import get_file_path, read_image
from api.session import UserSession

router = APIRouter()

require_bearer = HTTPBearer()


@router.post(
    "/morphology-image",
    dependencies=[Depends(require_bearer)],
    response_model=None,
    tags=["Morphology Image"],
)
def get_morphology_image(
    morpho_img_body: MorphoImageBody,
    user_session: UserSession = Depends(require_user_session),
) -> Union[FileResponse, None]:
    """
    Endpoint to get a preview image of a morphology
    """
    morpho_id = morpho_img_body.id

    authorization = f"Bearer {user_session.token}"
    response = requests.get(morpho_id, headers={"authorization": authorization})

    if response.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail=f"Something went wrong while fetching the morphology: {str(morpho_id)}",
        )

    morphology = response.json()

    distribution = next(
        (
            distribution
            for distribution in morphology["distribution"]
            if distribution["encodingFormat"] == "application/swc"
        ),
        None,
    )

    if distribution is None:
        raise HTTPException(
            status_code=500,
            detail=f"This morphology appears to not have an SWC distribution: {str(morphology)}",
        )

    content_url = distribution["contentUrl"]

    file_path = get_file_path(content_url)

    if os.path.isfile(file_path):
        return FileResponse(file_path, media_type="image/png")
    else:
        return read_image(authorization, content_url)
