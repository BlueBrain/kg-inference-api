from typing import List, Union, Dict, Tuple
import os
import requests
from query.forge import retrieve_elastic, to_result_resource
from data.rule import Rule
from data.result.result_sparql import ResultSparql
from data.dict_key import DictKey
from data.result.result import Result, Attribute
from data.result.result_resource import ResultResource
from config import API_BASE, ENVIRONMENT


def request(endpoint_rel, data, token):
    """
    Helper function to send a request to the API endpoint
    @param endpoint_rel: the relative url of the endpoint being targeted
    @param data: data to be added to the request's body in json format
    @param token: the user authentication token
    @return the body of the response in json format
    @raises APIError for any error unrelated to the authentication (can't reach the api,
    API Internal error)
    @raise AuthenticationError if the authentication fails (missing or invalid authentication token)
    """
    endpoint = os.path.join(API_BASE, endpoint_rel)
    headers = {"Authorization": f"Bearer {token}"}

    try:
        r = requests.post(endpoint, json=data, headers=headers, verify=False)
    except requests.exceptions.ConnectionError:
        raise APIError("Couldn't reach API")

    if r.status_code != 200:
        if r.status_code in (403, 401):
            body = r.json()
            raise AuthenticationError(body["detail"])

        try:
            body = r.json()
            raise APIError(body["detail"] if "detail" in body else "Rules: Internal Error")
        except requests.exceptions.JSONDecodeError as e:
            raise APIError("Rules: Internal Error") from e

    body = r.json()
    return body


class AuthenticationError(BaseException):
    """Raised when a request returns a status code 402"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class APIError(BaseException):
    """Raised when a request returns a status code different from 200"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def get_rules(token, search_filters: dict = None) -> List[Rule]:
    """
    Retrieves rules,
    @param token the user authentication token
    @param search_filters, optional a dictionary of filters with keys of type DictKey
    and the value one or a list of ids of an entity that corresponds to the DictKey type
    @return the list of Rule instances matching the search filters, or all rules if no filters
    are specified
    """
    endpoint_rel = "rules"

    data = {}

    if search_filters:
        rt = search_filters[DictKey.DATA_TYPES.value]

        if rt is not None and len(rt) > 0:
            data["resourceTypes"] = rt

        api_to_local_keys = {
            "CellTypeQueryParameter": DictKey.CELL_TYPES,
            "MTypeQueryParameter": DictKey.CELL_TYPES,
            "BrainRegionQueryParameter": DictKey.BRAIN_REGIONS
        }

        if any([key.value in search_filters for key in api_to_local_keys.values()]):
            data["inputFilters"] = dict([
                (api_key, search_filters[local_key.value])
                for api_key, local_key in api_to_local_keys.items()
                if local_key.value in search_filters and search_filters[local_key.value] is not None
            ])

    body = request(endpoint_rel=endpoint_rel, data=data, token=token)

    return [Rule.source_to_class(el) for el in body]


def infer(rule_id: str, input_parameters: dict, token: str, retrieve=True,
          use_sparql_minds=False) \
        -> Dict[str, Union[ResultResource, Tuple[ResultResource, ResultSparql], None]]:
    """
    Infer Resources by running a rule
    @param rule_id: the id of the rule to be run
    @param input_parameters: the input parameter values, as a dictionary of the rule
    @param token: the user authentication token
    @param retrieve whether only the ids are returned or the Resource information is being
    retrieved too
    @param use_sparql_minds whether to also run a sparql query to retrieve minds information for
    the inferred resources
    @return returns a dictionary with the keys being the ids of the resources that have been
    inferred,
    and the values being None if retrieve is False, ResultResources if retrieve is True
    and use_sparql_minds is False,
    pairs of ResultResource and ResultSparql if retrieved is True and use_sparql_minds is True
    """
    endpoint_rel = "infer"
    data = {
        "rules": [{"id": rule_id}],
        "inputFilter": input_parameters
    }
    body = request(endpoint_rel=endpoint_rel, data=data, token=token)

    if len(body) == 0 or "results" not in body[0]:
        return {}

    body = body[0]["results"]

    id_index = dict((body_i["id"], body_i) for body_i in body)

    if not retrieve:
        return dict(zip(id_index.keys(), [None] * len(id_index)))

    retrieved, forge = retrieve_elastic(list(id_index.keys()), token)
    resources: List[ResultResource] = to_result_resource(retrieved, forge=forge,
                                                         additional_data=id_index)

    # TODO NOT FINISHED YET (query + downstream usage), implement if ever we switch to this
    # if use_sparql_minds:
    #     retrievals = zip(resources, minds(ids=[r.get_attribute(Attribute.ID) for r in resources],
    #                                       token=token))
    # else:
    #     retrievals = resources

    return dict(
        (r.get_attribute(Attribute.ID), ResultResource.class_to_store(r))
        for r in resources
    )
