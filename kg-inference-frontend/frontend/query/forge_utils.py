from urllib.parse import quote_plus
from kgforge.core import KnowledgeGraphForge, Resource


def get_store(forge):
    return forge._store


def get_forge_org_project(forge: KnowledgeGraphForge):
    return get_store(forge).bucket.split("/")[-2:]


def get_resource_org_project(resource: Resource):
    return resource._store_metadata._project.split("/")[-2:]


def get_self(resource: Resource):
    return resource._store_metadata._self


def _get_new_search_endpoint(forge, new_view):
    org, project = get_forge_org_project(forge)

    return "/".join((
        get_store(forge).endpoint,
        "views",
        quote_plus(org),
        quote_plus(project),
        quote_plus(new_view),
        "_search"
    ))


def set_sparql_view(forge, new_view):
    endpoint = _get_new_search_endpoint(forge, new_view)
    get_store(forge).service.sparql_endpoint["endpoint"] = endpoint


def set_elastic_view(forge, new_view):
    endpoint = _get_new_search_endpoint(forge, new_view)
    get_store(forge).service.elastic_endpoint["endpoint"] = endpoint
