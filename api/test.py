from api.main import app
from api.config import NEXUS_TOKEN
from fastapi.testclient import TestClient

client = TestClient(app)


def get_headers():
    if NEXUS_TOKEN == "":
        raise Exception("Missing NEXUS_TOKEN")
    return {"Authorization": f"Bearer {NEXUS_TOKEN}"}


def test_get_all_rules():
    response = client.post("/rules", headers=get_headers())
    assert response.status_code == 200
    assert len(response.json()) == 7


def get_rules_resource_type(resource_type, expected_count):
    data = {"resourceTypes": [resource_type]}
    response = client.post("/rules", headers=get_headers(), json=data)
    assert response.status_code == 200
    assert len(response.json()) == expected_count


def test_get_rules_resource_trace():
    return get_rules_resource_type("Trace", 4)


def test_get_rules_resource_neuron_morphology():
    return get_rules_resource_type("NeuronMorphology", 6)
