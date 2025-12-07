import allure
from api.service_client import ServiceClient


def obtain_client_token(client_data):
    """Получение токена аутентификации для клиента"""
    auth_response = ServiceClient.authenticate_client(client_data["email"], client_data["password"])
    return auth_response.json()["accessToken"]


@allure.step('Получить токен аутентификации')
def obtain_client_token_with_step(client_data):
    """Получение токена аутентификации для клиента с allure-шагом"""
    return obtain_client_token(client_data)