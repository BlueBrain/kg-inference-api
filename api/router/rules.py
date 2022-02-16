from typing import List
from fastapi import APIRouter, Depends
from starlette.requests import Request
from api.dependencies import require_user_auth
from inference_tools.utils import fetch_rules
from api.models.rules import RuleOutput, RulesBody
from api.rules import RulesHandler
from api.utils import get_or_create_forge_session

router = APIRouter()


@router.post("", dependencies=[Depends(require_user_auth)], response_model=List[RuleOutput])
async def get_all_rules(request: Request,
                        user_params: dict = Depends(require_user_auth),
                        rules_body: RulesBody = None):
    """
    Endpoint to get all the data generalization rules

    :param rules_body:
    :param request:
    :param user_params:
    :return:
    """
    resource_types = None if rules_body is None else rules_body.resource_types
    forge = get_or_create_forge_session(request=request,
                                        username=user_params.get("user").username,
                                        access_token=user_params.get("access_token"))
    rules_view = "https://bbp.epfl.ch/neurosciencegraph/data/rule-view"
    rules = fetch_rules(forge, rules_view, resource_types=resource_types)
    rules_handler = RulesHandler(rules=rules)
    if rules_body and rules_body.input_filters:
        rules_handler.filter_rules(input_filters=rules_body.input_filters, token=user_params.get("access_token"))
    serialized_rules = rules_handler.serialize_rules()
    return serialized_rules
