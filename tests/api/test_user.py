from conftest import authenticated_user, super_admin
from models.base_models import TestUser, RegisterUserResponse
import pytest

def test_get_user_info(api_manager, authenticated_user):
    """Проверяем информацию о себе"""
    #Регистрируем и обновляем сессию
    user_data = authenticated_user
    user_id = user_data["id"]
    user_email = user_data["email"]

    #Отправляем запрос
    user_response = api_manager.user_api.get_user_info(user_id="me").json()
    user_id_after = user_response["id"]
    user_email_after = user_response["email"]

    #Проверяем email и id с ответом и который был в регистрации
    assert user_id_after == user_id, \
    f"Ожидали получил {user_id}, получили - {user_id_after}"
    assert user_email_after == user_email, \
    f"Ожидали получить {user_email}, получили - {user_email_after}"

def test_delete_users(api_manager, test_user, test_user_2, test_user_3, test_user_4, super_admin):
    #Регистрируем 3 пользователей
    first_user_response = api_manager.auth_api.register_user(test_user_4)
    second_user_response = api_manager.auth_api.register_user(test_user_2)
    third_user_response = api_manager.auth_api.register_user(test_user_3)

    #Проверяем валидность данных
    first_user_reg = RegisterUserResponse(**first_user_response.json())
    second_user_reg = RegisterUserResponse(**second_user_response.json())
    third_user_reg = RegisterUserResponse(**third_user_response.json())


    #Забираем их id
    first_user_id = first_user_reg.id
    second_user_id = second_user_reg.id
    third_user_id = third_user_reg.id

    #Удаляем их через метод
    super_admin.api.user_api.delete_user(first_user_id)
    super_admin.api.user_api.delete_user(second_user_id)
    super_admin.api.user_api.delete_user(third_user_id)

    #Проверяем, что они удалены
    for user in [test_user_4, test_user_2, test_user_3]:
        response = api_manager.auth_api.login_user({
            "email": user.email,
            "password": user.password
        }, expected_status=401)  # Ожидаем 401


class TestUser:

    def test_create_user(self, super_admin, creation_user_data):
        """
        Было:
        response = super_admin.api.user_api.create_user(creation_user_data).json()

        assert response.get('id') and response['id'] != '', "ID должен быть не пустым"
        assert response.get('email') == creation_user_data['email']
        assert response.get('fullName') == creation_user_data['fullName']
        assert response.get('roles', []) == creation_user_data['roles']
        assert response.get('verified') is True
        Cтало:
        """
        response = super_admin.api.user_api.create_user(creation_user_data)
        reg_response = RegisterUserResponse(**response.json())
        assert reg_response.email == creation_user_data.email, \
        f"Ожидаем, что email буду равны, получили {reg_response.email} и {creation_user_data.email}"
        assert reg_response.id is not None, "ID должен быть присвоен"
        assert reg_response.fullName == creation_user_data.fullName
        assert reg_response.roles == creation_user_data.roles
        assert reg_response.verified is True, "Пользователь должен быть верифицирован"

    def test_get_user_by_locator(self, super_admin, creation_user_data):
        """Тест получения пользователя по ID и email"""

        # Создаем пользователя
        create_response = super_admin.api.user_api.create_user(creation_user_data)
        created_user = RegisterUserResponse(**create_response.json())

        # Получаем пользователя по ID и по email
        response_by_id = super_admin.api.user_api.get_user(created_user.id)
        user_by_id = RegisterUserResponse(**response_by_id.json())

        response_by_email = super_admin.api.user_api.get_user(creation_user_data.email)
        user_by_email = RegisterUserResponse(**response_by_email.json())

        # Проверяем, что ответы идентичны
        assert user_by_id.model_dump() == user_by_email.model_dump(), \
            "Данные пользователя должны быть одинаковыми при запросе по ID и email"

        # Проверяем, что все поля соответствуют ожидаемым
        assert user_by_id.id == created_user.id, "ID должен совпадать с созданным"
        assert user_by_id.email == creation_user_data.email, "Email должен совпадать"
        assert user_by_id.fullName == creation_user_data.fullName, "FullName должен совпадать"
        assert user_by_id.roles == creation_user_data.roles, "Roles должны совпадать"
        assert user_by_id.verified is True, "Пользователь должен быть верифицирован"
        assert user_by_id.createdAt is not None, "Дата создания должна быть заполнена"

    def test_get_user_by_id_common_user(self, common_user):
        common_user.api.user_api.get_user(common_user.email, expected_status=403)

