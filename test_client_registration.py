import pytest
import allure
from api.service_client import ServiceClient
from api.data import generate_client_profile, ServiceResponse


@allure.feature('Регистрация клиента')
class TestClientRegistration:
    @allure.title('Успешная регистрация нового клиента')
    def test_register_new_client_successfully(self, cleanup_test_data):
        with allure.step('Создать тестовый профиль клиента'):
            client_profile = generate_client_profile()
            cleanup_test_data.update(client_profile)

        with allure.step('Выполнить запрос на регистрацию'):
            response = ServiceClient.register_client(client_profile)

        with allure.step('Проверить успешность регистрации'):
            assert response.status_code == 200
            assert response.json()["success"] == True
            assert response.json()["user"]["email"] == client_profile["email"]

    @allure.title('Невозможность регистрации существующего клиента')
    def test_register_existing_client_fails(self, setup_test_client):
        with allure.step('Получить данные активного клиента'):
            client_data = setup_test_client

        with allure.step('Повторно отправить запрос регистрации'):
            response = ServiceClient.register_client(client_data)

        with allure.step('Проверить сообщение о конфликте'):
            assert response.status_code == 403
            assert response.json() == ServiceResponse.CLIENT_EXISTS

    @pytest.mark.parametrize('required_field', ['email', 'password', 'name'])
    @allure.title('Проверка обязательных полей при регистрации: {required_field}')
    def test_registration_requires_all_fields(self, required_field):
        with allure.step('Создать профиль и удалить обязательное поле'):
            client_profile = generate_client_profile()
            client_profile.pop(required_field)

        with allure.step('Отправить запрос с отсутствующим полем'):
            response = ServiceClient.register_client(client_profile)

        with allure.step('Проверить ошибку валидации'):
            assert response.status_code == 403
            assert response.json() == ServiceResponse.INCOMPLETE_DATA