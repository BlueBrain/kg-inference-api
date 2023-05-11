from typing import Union, List, Dict, Tuple, Optional
import os
import json

from kgforge.core import KnowledgeGraphForge, Resource
from kgforge.core.commons.exceptions import QueryingError
from kgforge.core.wrappings.dict import DictWrapper
from requests.exceptions import HTTPError
from data.brain_region import BrainRegion
from data.data_type import DataType
from data.cell_type import CellType, MType, EType
from data.entity import Entity
from data.result.attribute import Attribute
from data.result.result import Result
from data.result.result_resource import ResultResource
from data.species import Species
from data.utils import get_id
from query.forge_utils import set_elastic_view, set_sparql_view
from query.sdk_layer import fetch as fetch_file
from config import NEXUS_ENDPOINT, NEXUS_CONFIG_PATH

shape_rule_id = "https://bbp.epfl.ch/neurosciencegraph/data/ac5885c8-bb70-4336-ae7f-3e1425356fe8"
all_aspect_rule_id = \
    "https://bbp.epfl.ch/neurosciencegraph/data/abb1949e-dc16-4719-b43b-ff88dabc4cb8"
location_rule_id = "https://bbp.epfl.ch/neurosciencegraph/data/70e8e757-1834-420c-bcc1-37ea850ddfe3"

NM_RULE_IDS = [shape_rule_id, location_rule_id, all_aspect_rule_id]


class ForgeError(BaseException):
    """Raised when an error occurs from forge """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


DEBUG = False

LIMIT = 10000


def _allocate_forge_session(org, project, token, config_path=NEXUS_CONFIG_PATH):
    try:
        forge = KnowledgeGraphForge(
            configuration=config_path,
            endpoint=NEXUS_ENDPOINT,
            token=token,
            bucket=f"{org}/{project}",
            debug=DEBUG
        )
    except HTTPError as e:
        raise ForgeError(str(e)) from e

    return forge


def get_forge_neuroscience_datamodels(token):
    return _allocate_forge_session("neurosciencegraph", "datamodels", token)


def get_forge_bbp_atlas(token):
    return _allocate_forge_session("bbp", "atlas", token)


def sparql_to_class(query_str, class_name, forge, limit=True):
    """
    Runs a sparql query, and turns the list dictionaries into a list of instances of the
    provided class. Optionally enforces a limit onto the query
    @param query_str: the Sparql query string
    @param class_name: the class into which the resulting dictionaries should be converted into
    @param forge: a forge instance to run the query
    @param limit: whether to apply a fixed limit
    @return a list of instances of the provided class
    """
    try:
        c = forge.sparql(query_str, limit=LIMIT if limit else None, debug=DEBUG, cross_bucket=True)
    except QueryingError as e:
        raise ForgeError(str(e))

    results = get_latest_revisions(forge.as_json(c))
    return [class_name.source_to_class(c) for c in results] if results else []


def get_species(forge):
    query_str = """
        SELECT ?id ?name ?_rev
        WHERE {
            ?id rdfs:subClassOf Species .
            ?id label ?name ;
                _deprecated  ?_deprecated ;
                _rev ?_rev
            FILTER (?_deprecated = 'false'^^xsd:boolean)  
        }
        """
    return sparql_to_class(query_str=query_str, class_name=Species, forge=forge)


def get_brain_regions(forge):
    query_str = """
        SELECT ?id ?name ?_rev
        WHERE {
            ?id rdfs:subClassOf* BrainRegion .
            ?id label ?name ;
                _deprecated  ?_deprecated ;
                _rev ?_rev
            FILTER (?_deprecated = 'false'^^xsd:boolean)  
        }
        """
    return sparql_to_class(query_str=query_str, class_name=BrainRegion, forge=forge)


def get_cell_types(forge):
    query_str = """
           SELECT ?id ?name ?_rev
           WHERE {
            ?id rdfs:subClassOf* bmo:BrainCellType .
            ?id label ?name ;
                _deprecated  ?_deprecated ;
                _rev ?_rev
            FILTER (?_deprecated = 'false'^^xsd:boolean)  
           }
       """
    return sparql_to_class(query_str=query_str, class_name=CellType, forge=forge)


def get_data_types(forge):
    query_str = """
        SELECT ?id ?name ?_rev
        WHERE {
            ?id rdfs:subClassOf* schema:Dataset .
            ?id label ?name ; 
                _deprecated ?_deprecated ;
                _rev ?_rev
            FILTER (?_deprecated = 'false'^^xsd:boolean)  
        }
    """
    return sparql_to_class(query_str=query_str, class_name=DataType, forge=forge)


def get_m_types(forge):
    query_str = """
        SELECT ?id ?name ?_rev
        WHERE {
            ?id rdfs:subClassOf* bmo:NeuronMorphologicalType .
            ?id label ?name ; 
                _deprecated ?_deprecated ;
                _rev ?_rev
            FILTER (?_deprecated = 'false'^^xsd:boolean)  
        }
    """
    return sparql_to_class(query_str=query_str, class_name=MType, forge=forge)


def get_e_types(forge):
    query_str = """
        SELECT ?id ?name ?_rev
        WHERE {
            ?id rdfs:subClassOf* bmo:NeuronElectricalType .
            ?id label ?name ; 
                _deprecated ?_deprecated ;
                _rev ?_rev
            FILTER (?_deprecated = 'false'^^xsd:boolean)  
        }
    """
    return sparql_to_class(query_str=query_str, class_name=EType, forge=forge)


def get_entities(forge):
    query_str = """
               SELECT ?id ?name ?_rev
               WHERE {
                ?id rdfs:subClassOf* prov:Entity.
                ?id label ?name ; 
                    _deprecated ?_deprecated .
                    _rev ?_rev
                FILTER (?_deprecated = 'false'^^xsd:boolean)  
               }
           """

    return sparql_to_class(query_str=query_str, class_name=Entity, forge=forge)


# TODO
def get_contributors(forge):
    return None


def download(resource, follow, path, token, org, project, is_json=True):
    """
    Downloads a file that is linked to a resource
    @resource the Resource
    @follow the path to follow within the resource to reach the file id(s)
    @path where the download the file
    @token the user authentication token
    @org the organisation the resource belongs to
    @project the project the resource belongs to
    @is_json whether the resource is in json format or a kgforge.core.Resource
    """
    forge = _allocate_forge_session(org, project, token)

    forge.download(data=forge.from_json(resource) if is_json else resource,
                   follow=follow, path=path)


def forge_retrieve(ids, token, to_result=False) -> \
        Union[List[Union[Resource, ResultResource]], Union[Resource, ResultResource]]:
    """
        From Resource id(s), retrieves a list or a singular kgforge.core.Resources
        and optionally converts them/it to a ResultResource
        @param ids: list of ids
        @param token: the user authentication token
        @param to_result: whether to convert the kgforge.core.Resource(s) into ResultResource(s)
        @return a list or a singular kgforge.core.Resource or ResultResource
    """
    if not isinstance(ids, list):
        ids = [ids]

    forge = get_forge_bbp_atlas(token)
    retrieved = [forge.retrieve(el, cross_bucket=True) for el in ids]

    if to_result:
        retrieved = [ResultResource.to_result_object(el, forge) for el in retrieved]

    return retrieved if (len(retrieved) > 1 or len(retrieved) == 0) else retrieved[0]


def forge_get_files(file_ids, token, org, project):
    """
    Using the nexussdk, gets files over http and returns them as a http Response object
    @param file_ids: the file ids
    @param token: the user authentication token
    @param org: the organisation the file belongs to
    @param project: the project the file belongs to
    @return a list of http Response from the file fetching
    """

    return [
        fetch_file(
            environment=NEXUS_ENDPOINT,
            token=token,
            org_label=org,
            project_label=project,
            file_id=file_id,
            out_filepath="return"
        )
        for file_id in file_ids
    ]


def forge_download_files(file_ids, token, path_to_download, org, project):
    """
         Using the nexussdk, gets files over http and downloads them into a specified location
         @param file_ids: the file ids
         @param token: the user authentication token
         @param path_to_download: the path where the file(s) will be downloaded
         @param org: the organisation the file belongs to
         @param project: the project the file belongs to
         @return a list of http Response from the file fetching
         """
    os.makedirs(path_to_download, exist_ok=True)

    files = [
        fetch_file(
            environment=NEXUS_ENDPOINT,
            token=token,
            org_label=org,
            project_label=project,
            file_id=file_id,
            out_filepath=f"{path_to_download}/"
        )
        for file_id in file_ids]

    return [el["_filename"] for el in files]


def get_latest_revisions(result_list: List[dict]) -> List[dict]:
    """
    Assuming a list of Resources (or rather, a subset of their properties and values)
    in a dictionary format, which results from a Sparql query, where a single Resource may be
    retrieved multiple times for different revisions, as specified by their "_rev" field,
    return only the Resource dictionaries with the latest revisions for each Resource
    @param result_list: the list of resources as dictionaries
    @return a filtered out list of Resources as dictionaries keeping only the latest revisions
    """
    temp = {}
    for val in result_list:  # organize into a dictionary of the same entity indexed by revisions
        temp.setdefault(val["id"], {}).update({val["_rev"]: val})

    return [temp[key][max(value.keys())] for key, value in
            temp.items()]  # get only the latest revision (max index)


def contribution_label_fill(result_resources: List[ResultResource], forge: KnowledgeGraphForge) -> \
        List[ResultResource]:
    """
    Fill the contribution label for all contributions in a ResultResource:
    when retrieving a Resource, it may have contributions. When it does, only their id is
    available. A label is necessary to display the contribution (either the Contribution entity's
    name or a concatenation of its firstName and lastName). For a list of ResultResources,
    all contribution entities are retrieved, the appropriate label is built, and the label field
    is added into the contribution dictionaries located within the ResultResources
    @param result_resources: the list of ResultResource
    @param forge: a forge instance to run the query
    @return the list of ResultResource with the contribution labels added
    """
    ids_to_fetch = set()
    for result_resource in result_resources:
        ids_to_fetch.update(set([contribution.id for contribution in result_resource.get_attribute(
            Attribute.CONTRIBUTION, to_str=False) if not contribution.label]))

    if len(ids_to_fetch) == 0:
        return result_resources

    res = [forge.retrieve(id_, cross_bucket=True) for id_ in ids_to_fetch]
    contributors = [forge.as_json(el) for el in res if el is not None]

    def get_label(contributor_json):
        if "name" in contributor_json:
            return contributor_json["name"]
        if "givenName" in contributor_json and "familyName" in contributor_json:
            return f"{contributor_json['givenName']} {contributor_json['familyName']}"
        return contributor_json["id"]

    id_label_map = dict((get_id(el), get_label(el)) for el in contributors)

    def add_contribution_label(resource):
        return resource.set_contributions([
            c.set_label(id_label_map.get(c.id, "?") if c.label is None else c.label)
            for c in result_resource.get_attribute(Attribute.CONTRIBUTION)
        ])

    return [add_contribution_label(resource) for resource in result_resources]


def stimulus_type_label_fill(result_resources: List[ResultResource], forge: KnowledgeGraphForge):
    """
       Fill the stimulus type label for all trace images in a ResultResource: when retrieving
        a Resource, it may have trace images characterized by stimulus types. When it does,
        only their id is available. A label is necessary to display the stimulus type.
       For a list of ResultResources, all stimulus type entities are retrieved,
       and the label field is added into the stimulus type dictionaries located within the
       ResultResources
       @param result_resources: the list of ResultResource
       @param forge: a forge instance to run the query
       @return the list of ResultResource with the stimulus type labels added
       """
    ids_to_fetch = set()

    for result_resource in result_resources:
        ids_to_fetch.update([
            get_id(image.stimulus_type)
            for image in result_resource.get_attribute(Attribute.IMAGE, to_str=False)
            if "label" not in image.stimulus_type
        ])

    if len(ids_to_fetch) == 0:
        return result_resources

    res = [forge.retrieve(id_, cross_bucket=True) for id_ in ids_to_fetch]

    stimuli = [forge.as_json(el) for el in res if el is not None]

    def get_obj(stimulus_type_resource):
        return {
            "id": get_id(stimulus_type_resource),
            "label": stimulus_type_resource.get("label", get_id(stimulus_type_resource))
        }

    id_st_map = dict((get_id(el), get_obj(el)) for el in stimuli)

    def add_stimulus_type_label(resource):
        return resource.set_images([
            im.set_stimulus_type(
                id_st_map.get(
                    get_id(im.stimulus_type),
                    get_obj(im.stimulus_type)
                )
            )
            for im in resource.get_attribute(Attribute.IMAGE)
            if im.stimulus_type and "label" not in im.stimulus_type
        ])

    return [add_stimulus_type_label(resource) for resource in result_resources]


def to_result_resource(resources: List[Resource], forge: KnowledgeGraphForge,
                       additional_data: Optional[Dict]):
    result_resources = [
        ResultResource.to_result_object(
            element, forge,
            score=(
                additional_data[element.id].get("score", None)
                if additional_data is not None else None
            ),
            score_breakdown=(
                additional_data[element.id].get("score_breakdown", None))
            if additional_data is not None else None
        )
        for element in resources
    ]
    result_resources = contribution_label_fill(result_resources=result_resources, forge=forge)
    result_resources = stimulus_type_label_fill(result_resources=result_resources, forge=forge)
    return result_resources


def retrieve_elastic(ids, token) -> Tuple[List[Resource], KnowledgeGraphForge]:
    """
    Retrieves Resources whose id are in the id list provided
    @param ids: the list of Resource ids
    @param token: the user authentication token
    @return a list of kgforge.core.Resource and the KnowledgeGraphForge instance used to retrieve
    them
    """
    forge = get_forge_bbp_atlas(token)

    q = {
        "from": 0,
        "size": 10000,
        'query': {
            'bool': {
                'filter': [
                    {'terms': {'@id': ids}}
                ],
                'must': [
                    {'match': {'_deprecated': False}}
                ],
                'must_not': [

                ]
            }
        },
    }

    resources = forge.elastic(json.dumps(q), debug=False)

    if resources is None:
        raise ForgeError("Elastic Search Retrieval was not successful")

    return resources, forge


# TODO finish
# def minds(ids, token) -> List[ResultSparql]:
#     """
#     Retrieve MINDs information of a list of Resources, provided a list of their ids,
#     and formats it into a ResultSparql instance
#     @param ids: the list of Resource ids
#     @param token: the user authentication token
#     @return a list of ResultSparql instances, holding MINDs information
#     """
#     forge = get_forge_bbp_atlas(token)
#
#     id_str = f"{' '.join([f'(<{id_i}>)' for id_i in ids])}"
#
#     query_str = """
#         SELECT ?id ?name ?_self ?_project
#         (GROUP_CONCAT(DISTINCT ?br_label; SEPARATOR=$SEP) AS ?brain_region)
#         (GROUP_CONCAT(DISTINCT ?subject_label; SEPARATOR=$SEP) AS ?subject)
#         (GROUP_CONCAT(DISTINCT ?type_i; SEPARATOR=$SEP) AS ?type)
#         (GROUP_CONCAT(DISTINCT ?contribution_name_i; SEPARATOR=$SEP) AS ?contribution_name)
#         (GROUP_CONCAT(DISTINCT ?contribution_i; SEPARATOR=$SEP) AS ?contribution)
#         (GROUP_CONCAT(DISTINCT ?class_label; SEPARATOR=$SEP) AS ?classification_label)
#         (GROUP_CONCAT(DISTINCT ?class_type; SEPARATOR=$SEP) AS ?classification_type)
#         (GROUP_CONCAT(DISTINCT ?distribution_cu_i; SEPARATOR=$SEP) AS ?distribution_content_url)
#         (GROUP_CONCAT(DISTINCT ?distribution_ef_i; SEPARATOR=$SEP) AS ?distribution_encoding_format)
#         (GROUP_CONCAT(DISTINCT ?distribution_al_i; SEPARATOR=$SEP) AS ?distribution_at_location)
#         (GROUP_CONCAT(DISTINCT ?image_i; SEPARATOR=$SEP) AS ?image)
#
#         WHERE {
#             ?id schema:name|rdfs:label ?name .
#             ?id _deprecated ?_deprecated .
#             ?id _self ?_self .
#             ?id _project ?_project .
#
#             OPTIONAL { ?id type ?type_i }
#             OPTIONAL {
#                 ?id nsg:brainLocation/nsg:brainRegion ?br .
#                 ?br label ?br_label
#             }
#             OPTIONAL {
#                 ?id nsg:subject/nsg:species ?subject .
#                 ?subject label ?subject_label
#             }
#             OPTIONAL { ?id distribution/contentUrl ?distribution_cu_i }
#             OPTIONAL { ?id distribution/encodingFormat ?distribution_ef_i }
#             OPTIONAL { ?id distribution/atLocation/location ?distribution_al_i }
#             OPTIONAL { ?id image ?image_i }
#             OPTIONAL { ?id contribution/agent ?contribution_i }
#             OPTIONAL {
#                 ?contribution_i givenName ?contribution_f_name .
#                 ?contribution_i familyName ?contribution_l_name .
#                 BIND(CONCAT(?contribution_f_name, ?contribution_l_name) AS ?contribution_name_i)
#             }
#             OPTIONAL { ?id annotation/hasBody/label ?class_label }
#             OPTIONAL { ?id annotation/hasBody/type ?class_type  }
#             OPTIONAL { ?contribution_i name ?contribution_name_i }
#
#             Filter (?_deprecated = 'false'^^xsd:boolean)
#             VALUES (?id) { $ID_LIST }
#         }
#         GROUP BY ?id ?name ?_self ?_project
#     """
#
#     query_str = query_str.replace("$ID_LIST", id_str)
#     query_str = query_str.replace("$SEP", '";"')
#
#     res = forge.sparql(query_str, debug=False)
#
#     if res is None:
#         raise ForgeError("Retrieving MINDs information failed")
#
#     if len(res) == 0:
#         return []
#
#     res_json = forge.as_json(res)
#
#     return [ResultSparql.to_result_object(res_i, forge) for res_i in res_json]


def download_from_content_url(content_url, content_type, path_to_download, org, project, token):
    """
    Download a file using only its content url, without having to follow a path within
    the Resource it's attached to
    @param content_url: the file content url
    @param content_type: the encoding format of the file
    @param path_to_download: the path where to download the file
    @param org: the organisation the file belongs to
    @param project: the project the file belongs to
    @param token: the user authentication token
    """
    forge = _allocate_forge_session("bbp", "atlas", token=token)
    forge._store._download_one(url=content_url, path=path_to_download,
                               store_metadata=DictWrapper({"_project": f"{org}/{project}"}),
                               cross_bucket=True, content_type=content_type,
                               bucket=f"{org}/{project}")


def get_neuron_morphologies(token: str, rule_id: str) -> Dict[str, Result]:

    forge_seu = _allocate_forge_session("bbp-external", "seu", token)

    q = {
        "from": 0,
        "size": 10000,
        "query": {
            "bool": {
                "must": [
                    {"term": {"_deprecated": False}},
                ]
            }
        }
    }

    set_elastic_view(forge_seu, "https://bbp.epfl.ch/neurosciencegraph/data/test_view")

    neuron_morphologies = forge_seu.elastic(json.dumps(q))

    limit_nm = 20
    if len(neuron_morphologies) > limit_nm:
        neuron_morphologies = neuron_morphologies[:limit_nm - 1]

    if neuron_morphologies is None:
        raise ForgeError("Elastic Search Retrieval was not successful")

    resources: List[ResultResource] = to_result_resource(neuron_morphologies, forge=forge_seu,
                                                         additional_data=None)

    return dict(
        (r.get_attribute(Attribute.ID), ResultResource.class_to_store(r))
        for r in resources
    )

# def get_neuron_morphologies_forge(token: str, rule_models: List[str]) -> Dict[str, Result]:
#     forge_seu = _allocate_forge_session("bbp-external", "seu", token)
#     # neuron_morphologies = forge_seu.search({
#     #     "type": "NeuronMorphology",
#     #     "id": {
#     #         "^derivation.entity.id": "id",
#     #         "id": rule_models
#     #     }
#     # })
#     # set_sparql_view(forge_seu, "https://bluebrain.github.io/nexus/vocabulary/defaultSparqlIndex")
#     neuron_morphologies = forge_seu.search({
#         "type": "NeuronMorphology",
#         "^entity/^derivation/generation/activity/used/id":
#             "https://bbp.epfl.ch/nexus/v1/resources/dke/embedding-pipelines/_/d0c21fd5-cb9c-445c"
#             "-b0a4-94847ba61f5a"}, debug=True)
#
#     resources: List[ResultResource] = to_result_resource(neuron_morphologies, forge=forge_seu)
#     return dict(
#         (r.get_attribute(Attribute.ID), ResultResource.class_to_store(r))
#         for r in resources
#     )
