from typing import List
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from kgforge.core import KnowledgeGraphForge
from api.dependencies import require_forge_session
from inference_tools.utils import fetch_rules
from api.models.rules import RuleOutput, RulesBody
from api.rules import RulesHandler

router = APIRouter()

require_bearer = HTTPBearer()


@router.post("", dependencies=[Depends(require_bearer)], response_model=List[RuleOutput])
async def get_all_rules(auth_credentials=Depends(require_bearer),
                        forge: KnowledgeGraphForge = Depends(require_forge_session),
                        rules_body: RulesBody = None):
    """
    Endpoint to get all the data generalization rules

    :param auth_credentials: the authentication credentials
    :param forge: the forge object
    :param rules_body: the body of the rules request
    :return:
    """
    resource_types = None if rules_body is None else rules_body.resource_types
    rules_view = "https://bbp.epfl.ch/neurosciencegraph/data/rule-view"
    # fetches rules using kg-inference lib
    rules = fetch_rules(forge, rules_view, resource_types=resource_types)
    rules_handler = RulesHandler(rules=rules)
    # if input filters are added in the request
    if rules_body and rules_body.input_filters:
        rules_handler.filter_rules(input_filters=rules_body.input_filters, token=auth_credentials.credentials)
    serialized_rules = rules_handler.serialize_rules()
    return serialized_rules
