from typing import List
from fastapi import APIRouter, Depends
from inference_tools.utils import fetch_rules
from starlette.requests import Request
from dependencies import require_nexus_project, require_user_auth
from models.rules import Rule
from serializer import Serializer
from utils import get_or_create_forge_session

router = APIRouter()


@router.get("", dependencies=[Depends(require_user_auth), Depends(require_nexus_project)], response_model=List[Rule])
async def get_all_rules(request: Request, user_params: dict = Depends(require_user_auth), bucket: str = Depends(require_nexus_project)):
    """
    Endpoint to get all the data generalization rules

    :param request:
    :param user_params:
    :param bucket:
    :return:
    """
    forge = get_or_create_forge_session(request=request,
                                        username=user_params.get("user").username,
                                        bucket=bucket,
                                        access_token=user_params.get("access_token"))
    rules_view = "https://bbp.epfl.ch/neurosciencegraph/data/rule-view"
    rules = fetch_rules(forge, rules_view)
    serialized_rules = Serializer.serialize_rules(rules)
    return serialized_rules
