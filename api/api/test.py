"""
Module: test_main.py

This module contains test cases for the KG Inference API using FastAPI's TestClient.
"""

from fastapi.testclient import TestClient
from api.main import app
from api.config import NEXUS_TOKEN

# Create a FastAPI TestClient instance
client = TestClient(app)


def get_headers() -> dict:
    """
    Returns the headers with the authorization token for the test client.

    Returns:
        dict: Headers with the authorization token.

    Raises:
        Exception: If the NEXUS_TOKEN is missing.
    """
    if NEXUS_TOKEN == "":
        raise RuntimeError("Missing NEXUS_TOKEN")
    return {"Authorization": f"Bearer {NEXUS_TOKEN}"}


def test_get_all_rules():
    """
    Test case for retrieving all rules from the "/rules" endpoint.
    """
    response = client.post("/rules", headers=get_headers())
    assert response.status_code == 200
    assert len(response.json()) == 7


def get_rules_resource_type(resource_type: str, expected_count: int):
    """
    Helper function for testing rule retrieval based on a specific resource type.

    Parameters:
        - resource_type (str): The resource type for which rules are to be retrieved.
        - expected_count (int): The expected count of rules for the specified resource type.
    """
    data = {"resourceTypes": [resource_type]}
    response = client.post("/rules", headers=get_headers(), json=data)
    assert response.status_code == 200
    assert len(response.json()) == expected_count


def test_get_rules_resource_trace():
    """
    Test case for retrieving rules related to the "Trace" resource type.
    """
    return get_rules_resource_type("Trace", 4)


def test_get_rules_resource_neuron_morphology():
    """
    Test case for retrieving rules related to the "NeuronMorphology" resource type.
    """
    return get_rules_resource_type("NeuronMorphology", 6)
