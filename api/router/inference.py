from typing import List
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from inference_tools.utils import apply_rule
from kgforge.core import KnowledgeGraphForge
from api.dependencies import require_forge_session
from api.models.inference import InferenceResult, InferenceBody

router = APIRouter()

require_bearer = HTTPBearer()


@router.post("", dependencies=[Depends(require_bearer)], response_model=List[InferenceResult])
async def infer_resources(inference_body: InferenceBody,
                          auth_credentials=Depends(require_bearer),
                          forge: KnowledgeGraphForge = Depends(require_forge_session)):
    """
    Receives a set of rules and an input filter and returns a set of inferred resources for each rule

    :param auth_credentials: the bearer token credentials
    :param forge: the forge object
    :param inference_body: the body of the inference request
    :return:
    """
    inference_results = []
    for rule in inference_body.rules:
        rule_json = forge.as_json(forge.retrieve(rule.id))
        # apply the rule to the filter
        results = apply_rule(rule=rule_json,
                             parameters=inference_body.input_filter,
                             token=auth_credentials.credentials)
        # if there are results, add it to the returned inference results
        if results:
            inference_results.append(InferenceResult(rule=rule.id, results=results))
    return inference_results
