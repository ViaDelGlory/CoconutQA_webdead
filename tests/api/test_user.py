from conftest import authenticated_user
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

def test_delete_users(api_manager, test_user, test_user_2, test_user_3, test_user_4, authenticated_admin):
    #Регистрируем 3 пользователей
    first_user_data = api_manager.auth_api.register_user(test_user_4).json()
    second_user_data = api_manager.auth_api.register_user(test_user_2).json()
    third_user_data = api_manager.auth_api.register_user(test_user_3).json()
    main_user = authenticated_admin
    first_user_id = first_user_data["id"]
    second_user_id = second_user_data["id"]
    third_user_id = third_user_data["id"]
    #Удаляем их через метод
    api_manager.user_api.delete_users(first_user_id,second_user_id,third_user_id)

    #Проверяем, что они удалены
    for user in [test_user_4, test_user_2, test_user_3]:
        response = api_manager.auth_api.login_user({
            "email": user["email"],
            "password": user["password"]
        }, expected_status=401)  # Ожидаем 401
