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
    Гарантирует наличие компонентов для тестов, иначе падает с понятной ошибкой."""
    try:
        response = requests.get(ServiceEndpoints.COMPONENTS_LIST)
        response.raise_for_status()
        data = response.json()
        
        if not data.get("success"):
            pytest.fail(f"API вернул неуспешный ответ: {data.get('message', 'Unknown error')}")
            
        if "data" not in data or not data["data"]:
            pytest.fail("API вернул пустой список компонентов")
            
        component_ids = [component["_id"] for component in data["data"][:2]]
        
        if not component_ids:
            pytest.fail("Не удалось извлечь ID компонентов из ответа")
            
        return component_ids
        
    except requests.RequestException as e:
        pytest.fail(f"Не удалось подключиться к API для получения компонентов: {e}")
    except (ValueError, KeyError) as e:
        pytest.fail(f"Некорректный формат ответа от API: {e}")