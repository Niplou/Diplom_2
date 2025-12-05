import pytest
import requests
from api.data import generate_client_profile, ServiceEndpoints
from api.service_client import ServiceClient


@pytest.fixture(scope="function")
def setup_test_client():
    client_profile = generate_client_profile()
    ServiceClient.register_client(client_profile)

    yield client_profile

    auth_response = ServiceClient.authenticate_client(client_profile["email"], client_profile["password"])
    access_token = auth_response.json()["accessToken"]

    ServiceClient.remove_client(access_token)


@pytest.fixture(scope="function")
def cleanup_test_data():
    client_data = {}

    yield client_data

    if client_data.get("email") and client_data.get("password"):
        auth_response = ServiceClient.authenticate_client(client_data["email"], client_data["password"])
        access_token = auth_response.json()["accessToken"]
        ServiceClient.remove_client(access_token)


@pytest.fixture(scope="session")
def fetch_available_components():
    response = requests.get(ServiceEndpoints.COMPONENTS_LIST)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    return [component["_id"] for component in data["data"][:2]]