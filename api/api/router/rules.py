from typing import List, Union, Dict
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from inference_tools.rules import fetch_rules

from api.dependencies import require_user_session
from api.models.rules import RuleOutput, RulesBody
from api.rules import RulesHandler
from api.session import UserSession

router = APIRouter()

require_bearer = HTTPBearer()


@router.post(
    "",
    dependencies=[Depends(require_bearer)],
    response_model=Union[List[RuleOutput], List[Dict]],
    tags=["Rules"]
)
def get_all_rules(
        user_session: UserSession = Depends(require_user_session), rules_body: RulesBody = None
) -> List[RuleOutput]:
    """
    Endpoint to get all the data generalization rules
    """
    resource_types = None if rules_body is None else rules_body.resource_types
    resource_ids = None if rules_body is None else rules_body.resource_ids
    rule_types = None if rules_body is None else rules_body.rule_types
    input_filters = None if rules_body is None else rules_body.input_filters
    # fetches rules using kg-inference lib

    rules = fetch_rules(
        forge_rules=user_session.get_rules_forge(),
        resource_types=resource_types,
        resource_ids=resource_ids,
        rule_types=rule_types,
        input_filters=input_filters,
        forge_factory=user_session.get_or_create_forge_session
    )

    return RulesHandler(rules=rules).serialize_rules()
