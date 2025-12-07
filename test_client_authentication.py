import pytest
import allure
from api.service_client import ServiceClient
from api.data import ServiceResponse, TestConstants


@allure.feature('Аутентификация клиента')
class TestClientAuthentication:

    @allure.title('Успешная аутентификация зарегистрированного клиента')
    def test_authenticate_existing_client_success(self, setup_test_client):
        client_data = setup_test_client

        with allure.step('Выполнить запрос аутентификации'):
            response = ServiceClient.authenticate_client(client_data["email"], client_data["password"])

        with allure.step('Проверить успешность входа'):
            assert response.status_code == 200
            assert response.json()["success"] == True
            assert response.json()["user"]["email"] == client_data["email"]

    @allure.title('Аутентификация с некорректным email')
    def test_authentication_fails_with_wrong_email(self, setup_test_client):
        with allure.step('Использовать несуществующий email'):
            client_data = setup_test_client
            incorrect_email = TestConstants.INVALID_CREDENTIAL

        with allure.step('Отправить запрос с неверным email'):
            response = ServiceClient.authenticate_client(incorrect_email, client_data["password"])

        with allure.step('Проверить ошибку аутентификации'):
            assert response.status_code == 401
            assert response.json() == ServiceResponse.AUTHENTICATION_FAILED

    @allure.title('Аутентификация с некорректным паролем')
    def test_authentication_fails_with_wrong_password(self, setup_test_client):
        with allure.step('Использовать неверный пароль'):
            client_data = setup_test_client
            incorrect_password = TestConstants.INVALID_CREDENTIAL

        with allure.step('Отправить запрос с неверным паролем'):
            response = ServiceClient.authenticate_client(client_data["email"], incorrect_password)

        with allure.step('Проверить ошибку аутентификации'):
            assert response.status_code == 401
            assert response.json() == ServiceResponse.AUTHENTICATION_FAILED