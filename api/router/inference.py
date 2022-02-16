from typing import List
from fastapi import APIRouter, Depends
from inference_tools.utils import apply_rule
from starlette.requests import Request
from dependencies import require_user_auth
from models.inference import InferenceResult, InferenceBody
from utils import get_or_create_forge_session

router = APIRouter()


@router.post("", dependencies=[Depends(require_user_auth)], response_model=List[InferenceResult])
async def infer_resources(request: Request,
                          inference_body: InferenceBody,
                          user_params: dict = Depends(require_user_auth)):
    """
    Receives a set of rules and an input filter and returns a set of inferred resources for each rule

    :param request:
    :param inference_body: the body of the inference request
    :param user_params: the authentication parameters
    :return:
    """
    forge = get_or_create_forge_session(request=request,
                                        username=user_params.get("user").username,
                                        access_token=user_params.get("access_token"))
    inference_results = []
    for rule in inference_body.rules:
        rule_json = forge.as_json(forge.retrieve(rule.id))
        # apply the rule to the filter
        results = apply_rule(rule=rule_json,
                             parameters=inference_body.input_filter,
                             token=user_params.get("access_token"))
        # if there are results, add it to the returned inference results
        if results:
            inference_results.append(InferenceResult(rule=rule.id, results=results))
    return inference_results
