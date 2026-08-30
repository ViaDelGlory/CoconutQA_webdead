from http.client import responses
import requests
import pytest
from conftest import api_manager
from models.base_models import RegisterUserResponse, TestUser
from clients.api_manager import ApiManager
import allure
from pytest_check import check
import datetime
from constants.roles import Roles

@allure.suite("Cinescope API Tests")
@allure.title("Тесты для регистрация/аутентификации сервиса Cinescope")
@allure.severity(allure.severity_level.CRITICAL)
@allure.label("qa_name", "webdead")
class TestAuth():
    def test_login(self, api_manager, registration_user_data, login_data):
        """Тест на логин"""
        with allure.step("Регистрируем нового тестового пользователя"):
            response = api_manager.auth_api.register_user(registration_user_data)
            register_user_response = RegisterUserResponse(**response.json())

        with allure.step("Забрали из фикстуры модели регистрации логин и пароль и логинимся с данными"):
            login_response = api_manager.auth_api.login_user(login_data)
            token = login_response.json()["accessToken"]

        with allure.step("Проверяем, что email совпадает и токен не пустой"):
            assert register_user_response.email == registration_user_data.email, "Email не совпадает"
            assert token is not None

    def test_register_user(self, api_manager: ApiManager, registration_user_data):
        """Регистрация под существующем пользователем"""
        with allure.step("Регистрируем нового тестового пользователя"):
            response = api_manager.auth_api.register_user(
                user_data=registration_user_data.model_dump(mode='json', exclude_none=True))
            register_user_response = RegisterUserResponse(**response.json())

        with allure.step("Проверяем, что email совпадает"):
            assert register_user_response.email == registration_user_data.email, "Email не совпадает"

    def test_logout(self, api_manager, login_data, registration_user_data):
        """Тест на логаут"""
        with allure.step("Регистрируем нового тестового пользователя"):
            response = api_manager.auth_api.register_user(registration_user_data)
            register_user_response = RegisterUserResponse(**response.json())
            assert register_user_response.email == registration_user_data.email, "Email не совпадает"

        with allure.step("Логинимся под зарегистрированным пользователем"):
            login_response = api_manager.auth_api.login_user(login_data)
            token = login_response.json()["accessToken"]
            refresh_token = api_manager.auth_api.session.cookies.get("refresh_token")
            assert token is not None

        with allure.step("Проверяем наличие рефреш токена в сессии"):
            assert api_manager.auth_api.session.cookies.get("refresh_token") == refresh_token

        with allure.step("Выходим из системы"):
            logout_response = api_manager.auth_api.logout_user()
            assert logout_response.text == "OK"

        with allure.step("Проверяем, что refresh_token удален или установлен в пустую строку"):
            current_refresh_token = api_manager.auth_api.session.cookies.get("refresh_token")
            assert current_refresh_token is None or current_refresh_token == "", \
                f"Ожидаем, что refresh_token будет пустой, получено: {current_refresh_token}"

    def test_login_and_update(self, api_manager, login_data, registration_user_data):
        """Получаем токен, обновляем нашу сессию и обращаемся с токеном к защищенному ресурсу"""
        with allure.step("Регистрируем нового тестового пользователя"):
            reg_response = api_manager.auth_api.register_user(registration_user_data)
            register_user_response = RegisterUserResponse(**reg_response.json())
            assert register_user_response.email == registration_user_data.email, "Email не совпадает"

        with allure.step("Логинимся под зарегистрированным пользователем"):
            response = api_manager.auth_api.login_user(login_data)

        with allure.step("Забираем токен из ответа и обновляем сессию"):
            login_token = response.json()["accessToken"]
            api_manager.auth_api._update_session_headers({"Authorization": "Bearer " + login_token})

        with allure.step("Проверяем, что Authorization заголовок добавился в сессию"):
            assert api_manager.session.headers.get("Authorization") == f"Bearer {login_token}", \
                f"Ожидаем Authorization: Bearer {login_token}, получили - {api_manager.session.headers}"

        with allure.step("Обращаемся к защищенному ресурсу с токеном (/user/me)"):
            get_response = api_manager.auth_api.send_request(
                "GET",
                "/user/me",
                expected_status=200
            )
            user_data = get_response.json()
            assert user_data.get("email") == login_data["email"]

    def test_login_and_update_uncorrected(self, api_manager):
        """Логинимся с некорректным паролем"""
        with allure.step("Подготавливаем данные для входа с некорректным паролем"):
            data = {
                "email": "Fasd23@email.com",
                "password": "Zxcasdqw313-"
            }

        with allure.step("Пытаемся залогиниться с некорректными данными"):
            response = api_manager.auth_api.login_user(data, expected_status=401)

        with allure.step("Проверяем, что сервер вернул статус 401 Unauthorized"):
            assert response.status_code == 401, \
                f"Ожидали 401, получили {response.status_code}"

    def test_register_timeout(self, api_manager, test_user):
        """Тест на таймаут при регистрации"""
        with allure.step("Пытаемся зарегистрировать пользователя с таймаутом 0.001 секунды"):
            with pytest.raises(requests.exceptions.ReadTimeout):
                api_manager.auth_api.register_user(test_user, timeout=0.001)

@allure.title("Тест регистрации пользователя с помощью Mock")
@allure.severity(allure.severity_level.MINOR)
@allure.label("qa_name", "Ivan Petrovich")
def test_register_user_mock(api_manager: ApiManager, test_user: TestUser, mocker):
    with allure.step(" Мокаем метод register_user в auth_api"):
        mock_response = RegisterUserResponse(  # Фиктивный ответ
            id="id",
            email="email@email.com",
            fullName="fullName",
            verified=True,
            banned=False,
            roles=[Roles.SUPER_ADMIN],
            createdAt=str(datetime.datetime.now())
        )

        mocker.patch.object(
            api_manager.auth_api,  # Объект, который нужно замокать
            'register_user',  # Метод, который нужно замокать
            return_value=mock_response  # Фиктивный ответ
        )

    with allure.step("Вызываем метод, который должен быть замокан"):
        register_user_response = api_manager.auth_api.register_user(test_user)

    with allure.step("Проверяем, что ответ соответствует ожидаемому"):
        with allure.step("Проверка поля персональных данных"):  # обратите внимание на вложенность allure.step
            with check:
                # Строка ниже выдаст исклющение и но выполнение теста продолжится
                check.equal(register_user_response.fullName, "INCORRECT_NAME", "НЕСОВПАДЕНИЕ fullName")
                check.equal(register_user_response.email, mock_response.email)

        with allure.step("Проверка поля banned"):
            with check("Проверка поля banned"):  # можно использовать вместо allure.step
                check.equal(register_user_response.banned, mock_response.banned)