from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from pydantic import Json
from starlette.requests import Request
from api.dependencies import require_nexus_project, require_user_auth
from inference_tools.utils import fetch_rules
from api.models.rules import Rule
from api.rules import RulesHandler
from api.utils import get_or_create_forge_session

router = APIRouter()


@router.get("", dependencies=[Depends(require_user_auth), Depends(require_nexus_project)], response_model=List[Rule])
async def get_all_rules(request: Request,
                        user_params: dict = Depends(require_user_auth),
                        bucket: str = Depends(require_nexus_project),
                        resource_type: Optional[List[str]] = Query(None),
                        input_filter: Optional[List[Json]] = Query(None)):
    """
    Endpoint to get all the data generalization rules

    :param input_filter:
    :param request:
    :param user_params:
    :param bucket:
    :param resource_type:
    :return:
    """
    forge = get_or_create_forge_session(request=request,
                                        username=user_params.get("user").username,
                                        bucket=bucket,
                                        access_token=user_params.get("access_token"))
    rules_view = "https://bbp.epfl.ch/neurosciencegraph/data/rule-view"
    rules = fetch_rules(forge, rules_view, resource_types=resource_type)
    rules_handler = RulesHandler(rules=rules)
    if input_filter:
        rules_handler.filter_rules(input_filters=input_filter, token=user_params.get("access_token"))
    serialized_rules = rules_handler.serialize_rules()
    return serialized_rules
