import random
import string
import time

class ServiceEndpoints:
    SERVICE_BASE = 'https://stellarburgers.nomoreparties.site'
    
    # Клиент: регистрация и аутентификация
    CLIENT_REGISTRATION = f'{SERVICE_BASE}/api/auth/register'
    CLIENT_AUTHENTICATION = f'{SERVICE_BASE}/api/auth/login'
    CLIENT_PROFILE = f'{SERVICE_BASE}/api/auth/user'
    
    # Компоненты и транзакции
    COMPONENTS_LIST = f'{SERVICE_BASE}/api/ingredients'
    TRANSACTION_RECORDS = f'{SERVICE_BASE}/api/orders'


class ServiceResponse:
    # клиент уже зарегистрирован
    CLIENT_EXISTS = {
        "success": False,
        "message": "User already exists"
    }

    # отсутствуют обязательные поля
    INCOMPLETE_DATA = {
        "success": False,
        "message": "Email, password and name are required fields"
    }

    # ошибка аутентификации
    AUTHENTICATION_FAILED = {
        "success": False,
        "message": "email or password are incorrect"
    }

    # требуется аутентификация
    AUTHENTICATION_REQUIRED = {
        "success": False,
        "message": "You should be authorised"
    }

    # отсутствуют компоненты
    MISSING_COMPONENTS = {
        "success": False,
        "message": "Ingredient ids must be provided"
    }


class TestConstants:
    # тестовые учетные данные
    INVALID_CREDENTIAL = 'test_credential_456_qwerty'
    
    # невалидные идентификаторы компонентов
    INVALID_COMPONENT_IDS = ["test-component-id-456-qwerty"]


def generate_client_profile():
    """Генератор тестовых профилей клиентов без использования Faker"""
    timestamp = int(time.time())
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    
    name = f"TestClient{timestamp}"
    password = f"Pass{timestamp}{random_suffix}!"
    email = f"client{timestamp}@testdomain.com"
    
    return {
        "email": email,
        "password": password,
        "name": name
    }


def generate_product_data():
    """Генератор данных продукта для расширения функциональности"""
    return {
        "title": f"Product_{random.randint(1000, 9999)}",
        "price": round(random.uniform(10.0, 1000.0), 2),
        "category": random.choice(["electronics", "clothing", "books"])
    }