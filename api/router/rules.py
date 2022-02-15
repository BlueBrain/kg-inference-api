from typing import List, Optional
from fastapi import APIRouter, Depends, Body
from starlette.requests import Request
from api.dependencies import require_user_auth
from inference_tools.utils import fetch_rules
from api.models.rules import Rule
from api.rules import RulesHandler
from api.utils import get_or_create_forge_session

router = APIRouter()


@router.post("", dependencies=[Depends(require_user_auth)], response_model=List[Rule])
async def get_all_rules(request: Request,
                        user_params: dict = Depends(require_user_auth),
                        resourceTypes: Optional[List[str]] = None,
                        inputFilters: Optional[List] = None):
    """
    Endpoint to get all the data generalization rules

    :param inputFilters:
    :param resourceTypes:
    :param request:
    :param user_params:
    :return:
    """
    forge = get_or_create_forge_session(request=request,
                                        username=user_params.get("user").username,
                                        access_token=user_params.get("access_token"))
    rules_view = "https://bbp.epfl.ch/neurosciencegraph/data/rule-view"
    rules = fetch_rules(forge, rules_view, resource_types=resourceTypes)
    rules_handler = RulesHandler(rules=rules)
    if inputFilters:
        rules_handler.filter_rules(input_filters=inputFilters, token=user_params.get("access_token"))
    serialized_rules = rules_handler.serialize_rules()
    return serialized_rules
