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
    """Фикстура для получения доступных компонентов.
    Возвращает список ID компонентов или пустой список в случае ошибки."""
    try:
        response = requests.get(ServiceEndpoints.COMPONENTS_LIST)
        response.raise_for_status()  # Вызовет исключение при коде состояния >= 400
        data = response.json()
        
        if data.get("success") and "data" in data:
            return [component["_id"] for component in data["data"][:2]]
        else:
            # Если структура ответа не соответствует ожидаемой
            return []
    except (requests.RequestException, ValueError, KeyError) as e:
        # Логируем ошибку, но не падаем
        print(f"Warning: Could not fetch components from {ServiceEndpoints.COMPONENTS_LIST}: {e}")
        return []