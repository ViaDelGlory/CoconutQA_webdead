import allure
import pytest
from playwright.sync_api import expect

@allure.epic("Тестирование UI")
@allure.feature("Авторизация")
@pytest.mark.ui
class TestLoginPage:

    @allure.title("Успешная регистрация и авторизация нового пользователя")
    def test_login(self, login_page, register_data, register_page, page):
        register_page.register(
            full_name=register_data["full_name"],
            email=register_data["email"],
            password=register_data["password"]
        )

        expect(page.get_by_text("Подтвердите свою почту")).to_be_visible()

        login_page.open()

        login_page.login(
            register_data["email"],
            register_data["password"]
        )

        expect(page).to_have_url(login_page.home_url)
        expect(page.get_by_text("Вы вошли в аккаунт")).to_be_visible()
