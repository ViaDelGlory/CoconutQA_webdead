from http.client import responses
import requests
import pytest
from conftest import api_manager


def test_login(api_manager, test_user, login_data):
    """Тест на логин"""
    #Регаем нового пользака
    api_manager.auth_api.register_user(test_user)

    #Логинимся теперь
    login_response = api_manager.auth_api.login_user(login_data)
    token = login_response.json()["accessToken"]
    assert token is not None


def test_register_user(api_manager, test_user):
    """Регистрация под существующем пользователем"""
    response = api_manager.auth_api.register_user(test_user)
    assert response.json()["email"] == test_user["email"]

def test_logout(api_manager, login_data, test_user):
    """Тест на логаут"""
    #Регаем нового пользака
    api_manager.auth_api.register_user(test_user)

    #Логинимся теперь
    login_response = api_manager.auth_api.login_user(login_data)
    token = login_response.json()["accessToken"]
    refresh_token = api_manager.auth_api.session.cookies.get("refresh_token")
    assert token is not None

    #Проверяем наличие рефреш токена в сессии
    assert api_manager.auth_api.session.cookies.get("refresh_token") == refresh_token

    #Выходим
    logout_response = api_manager.auth_api.logout_user()
    assert logout_response.text == "OK"
    assert api_manager.auth_api.session.cookies.get("refresh_token") is None, \
    f"Ожидаем, что refresh_token будет пустой"


def test_login_and_update(api_manager, login_data, test_user):
    """Получаем токен, обновляем нашу сессию и обращаемся с токеном в защищенному ресурсу"""
    #Регаем нового пользователя
    reg_response = api_manager.auth_api.register_user(test_user)
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

def test_login_and_update_uncorrected(custom_requester):
    """Логинимся с некертным паролем"""
    response = custom_requester.send_request(
        "POST",
        "/login",
        data={"email": "Fasd23@email.com", "password": "Zxcasdqw313-"},
        expected_status = 401,
        need_logging=True
    )

    assert response.status_code == 401, \
    f"Ожидали 401, получили {response.status_code}"

def test_register_timeout(api_manager, test_user):
    with pytest.raises(requests.exceptions.ConnectTimeout):
        api_manager.auth_api.register_user(test_user, timeout=0.001)



