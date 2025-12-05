import pytest
import allure
from api.service_client import ServiceClient
from api.data import ServiceResponse, TestConstants


def obtain_client_token(client_data):
    """Получение токена аутентификации для клиента"""
    auth_response = ServiceClient.authenticate_client(client_data["email"], client_data["password"])
    return auth_response.json()["accessToken"]


@allure.feature('Создание транзакции')
class TestTransactionCreation:

    @allure.title('Создание транзакции с аутентификацией и валидными компонентами')
    def test_create_transaction_with_auth_success(self, setup_test_client, fetch_available_components):
        client_data = setup_test_client

        with allure.step('Получить токен аутентификации'):
            auth_token = obtain_client_token(client_data)

        with allure.step('Создать транзакцию с компонентами'):
            response = ServiceClient.create_transaction(fetch_available_components, auth_token)

        with allure.step('Проверить успешность создания'):
            assert response.status_code == 200
            assert response.json()["success"] == True

    @allure.title('Создание транзакции без компонентов')
    def test_create_transaction_without_components_fails(self, setup_test_client):
        client_data = setup_test_client

        with allure.step('Получить токен аутентификации'):
            auth_token = obtain_client_token(client_data)

        with allure.step('Отправить запрос с пустым списком компонентов'):
            response = ServiceClient.create_transaction([], auth_token)

        with allure.step('Проверить ошибку валидации'):
            assert response.status_code == 400
            assert response.json() == ServiceResponse.MISSING_COMPONENTS

    @allure.title('Создание транзакции с неверными идентификаторами компонентов')
    def test_create_transaction_with_invalid_component_ids(self, setup_test_client):
        client_data = setup_test_client

        with allure.step('Получить токен аутентификации'):
            auth_token = obtain_client_token(client_data)

        with allure.step('Использовать некорректные идентификаторы'):
            response = ServiceClient.create_transaction(TestConstants.INVALID_COMPONENT_IDS, auth_token)

        with allure.step('Проверить внутреннюю ошибку сервера'):
            assert response.status_code == 500

    @allure.title('Создание транзакции без аутентификации')
    def test_create_transaction_without_auth_fails(self, fetch_available_components):
        with allure.step('Отправить запрос без токена'):
            response = ServiceClient.create_transaction(fetch_available_components)

        with allure.step('Проверить ошибку авторизации'):
            assert response.status_code == 401
            assert response.json() == ServiceResponse.AUTHENTICATION_REQUIRED