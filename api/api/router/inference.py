from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from inference_tools.execution import apply_rule
from inference_tools.source.elastic_search import ElasticSearch
from kgforge.core import Resource

from api.dependencies import require_user_session
from api.models.inference import InferenceResult, InferenceBody
from api.session import UserSession

router = APIRouter()

require_bearer = HTTPBearer()


@router.post("", dependencies=[Depends(require_bearer)],
             response_model=List[InferenceResult], tags=["Inference"])
def infer_resources(
        inference_body: InferenceBody,
        user_session: UserSession = Depends(require_user_session)
):
    """
    Receives a set of rules and an input filter and returns a set of inferred resources for
    each rule
    """
    rules_forge = user_session.get_rules_forge()
    inference_results = []

    try:
        for rule in inference_body.rules:

            rule_resource: Resource = ElasticSearch.get_by_id(forge=rules_forge, ids=rule.id)
            rule_json = rules_forge.as_json(rule_resource)
            # apply the rule to the filter
            results = apply_rule(
                forge_factory=user_session.get_or_create_forge_session,
                rule=rule_json,
                parameter_values=inference_body.input_filter,
                premise_check=True, debug=False
            )
            # if there are results, add it to the returned inference results
            if results:
                inference_results.append(InferenceResult(rule=rule.id, results=results))

        return inference_results
    except BaseException as e:
        raise HTTPException(
            status_code=400,
            detail=f"Something went wrong while applying inference: {str(e)}"
        )
