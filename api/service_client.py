import requests
import allure
from .data import ServiceEndpoints


class ServiceClient:
    @staticmethod
    @allure.step('Регистрация нового клиента')
    def register_client(profile_data):
        return requests.post(ServiceEndpoints.CLIENT_REGISTRATION, json=profile_data)

    @staticmethod
    @allure.step('Аутентификация клиента')
    def authenticate_client(email, passkey):
        return requests.post(ServiceEndpoints.CLIENT_AUTHENTICATION, json={"email": email, "password": passkey})

    @staticmethod
    @allure.step('Удаление профиля клиента')
    def remove_client(auth_token):
        headers = {"Authorization": auth_token}
        return requests.delete(ServiceEndpoints.CLIENT_PROFILE, headers=headers)

    @staticmethod
    def create_transaction(components, auth_token=None):
        headers = {}
        if auth_token:
            clean_token = auth_token.replace("Bearer ", "")
            headers["Authorization"] = f"Bearer {clean_token}"
        payload = {"ingredients": components}
        return requests.post(ServiceEndpoints.TRANSACTION_RECORDS, json=payload, headers=headers)
