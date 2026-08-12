from http.client import responses
import requests
import pytest
from conftest import api_manager
from models.base_models import RegisterUserResponse, TestUser
from clients.api_manager import ApiManager


def test_login(api_manager, registration_user_data, login_data):
    """Тест на логин"""
    #Регаем нового пользака
    response = api_manager.auth_api.register_user(registration_user_data)
    register_user_response = RegisterUserResponse(**response.json())

    #Логинимся теперь
    login_response = api_manager.auth_api.login_user(login_data)
    token = login_response.json()["accessToken"]
    assert register_user_response.email == registration_user_data.email, "Email не совпадает"
    assert token is not None


def test_register_user(api_manager: ApiManager, registration_user_data):
    """Регистрация под существующем пользователем"""
    response = api_manager.auth_api.register_user(user_data=registration_user_data.model_dump(mode='json', exclude_none=True))
    register_user_response = RegisterUserResponse(**response.json())
    assert register_user_response.email == registration_user_data.email, "Email не совпадает"


def test_logout(api_manager, login_data, registration_user_data):
    """Тест на логаут"""
    # Регаем нового пользака
    response = api_manager.auth_api.register_user(registration_user_data)
    register_user_response = RegisterUserResponse(**response.json())
    assert register_user_response.email == registration_user_data.email, "Email не совпадает"

    # Логинимся теперь
    login_response = api_manager.auth_api.login_user(login_data)
    token = login_response.json()["accessToken"]
    refresh_token = api_manager.auth_api.session.cookies.get("refresh_token")
    assert token is not None

    # Проверяем наличие рефреш токена в сессии
    assert api_manager.auth_api.session.cookies.get("refresh_token") == refresh_token

    # Выходим
    logout_response = api_manager.auth_api.logout_user()
    assert logout_response.text == "OK"

    # Проверяем, что refresh_token удален или установлен в пустую строку
    current_refresh_token = api_manager.auth_api.session.cookies.get("refresh_token")
    assert current_refresh_token is None or current_refresh_token == "", \
        f"Ожидаем, что refresh_token будет пустой, получено: {current_refresh_token}"


def test_login_and_update(api_manager, login_data, registration_user_data):
    """Получаем токен, обновляем нашу сессию и обращаемся с токеном в защищенному ресурсу"""
    # Регаем нового пользака
    reg_response = api_manager.auth_api.register_user(registration_user_data)
    register_user_response = RegisterUserResponse(**reg_response.json())
    assert register_user_response.email == registration_user_data.email, "Email не совпадает"

    #Логинимся под данными
    response = api_manager.auth_api.login_user(login_data)

    # Забираем токен из запроса и обновляем сессию
    login_token = response.json()["accessToken"]
    api_manager.auth_api._update_session_headers({"Authorization": "Bearer " + login_token})

    #Проверяем, что он добавился
    assert api_manager.session.headers.get("Authorization") == f"Bearer {login_token}", \
        f"Ожидаем Authorization: Bearer {login_token}, получили - {api_manager.session.headers}"

    #Обращаемся теперь к защищенному ресурсу с токеном
    get_response = api_manager.auth_api.send_request(
        "GET",
        "/user/me",
        expected_status = 200
    )
    user_data = get_response.json()
    assert user_data.get("email") == login_data["email"]

def test_login_and_update_uncorrected(api_manager):
    """Логинимся с некорректным паролем"""

    data = {
        "email": "Fasd23@email.com",
        "password": "Zxcasdqw313-"
    }

    response = api_manager.auth_api.login_user(data, expected_status=401)
    assert response.status_code == 401, \
    f"Ожидали 401, получили {response.status_code}"

def test_register_timeout(api_manager, test_user):
    with pytest.raises(requests.exceptions.ConnectTimeout):
        api_manager.auth_api.register_user(test_user, timeout=0.001)



