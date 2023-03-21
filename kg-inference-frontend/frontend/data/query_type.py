from enum import Enum


class QueryType(Enum):
    SPARQL_QUERY = "SparqlQuery"
    FORGE_SEARCH_QUERY = "ForgeSearchQuery"
    ELASTIC_SEARCH_QUERY = "ElasticSearchQuery"
