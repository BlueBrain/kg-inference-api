from typing import List
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from inference_tools.rules import fetch_rules
from api.dependencies import require_user_session
from api.models.rules import RuleOutput, RulesBody
from api.rules import RulesHandler
from api.session import UserSession

router = APIRouter()

require_bearer = HTTPBearer()


@router.post("", dependencies=[Depends(require_bearer)], response_model=List[RuleOutput],
             tags=["Rules"])
def get_all_rules(user_session: UserSession = Depends(require_user_session), rules_body: RulesBody = None):
    """
    Endpoint to get all the data generalization rules

    :param user_session: the user session as generated from the dependency
    :param rules_body: the body of the rules request
    :return:
    """
    resource_types = None if rules_body is None else rules_body.resource_types
    rules_view = "https://bbp.epfl.ch/neurosciencegraph/data/rule_view"
    # fetches rules using kg-inference lib
    rules = fetch_rules(forge_rules=user_session.get_rules_forge(),
                        forge_datamodels=user_session.get_datamodels_forge(),
                        rule_view_id=rules_view,
                        resource_types=resource_types)
    rules_handler = RulesHandler(rules=rules)
    # if input filters are added in the request
    if rules_body and rules_body.input_filters:
        rules_handler.filter_rules(input_filters=rules_body.input_filters,
                                   user_session=user_session)
    serialized_rules = rules_handler.serialize_rules()
    return serialized_rules
