import allure
import pytest
from playwright.sync_api import expect

@allure.epic("Тестирование UI")
@allure.feature("Отзывы")
@pytest.mark.ui
class TestMovieReview:

    @allure.title("Успешное добавление отзыва к фильму")
    def test_add_review(
        self,
        register_page,
        login_page,
        movies_page,
        movie_page,
        register_data,
        page
    ):
        register_page.open()
        register_page.register(
            full_name=register_data["full_name"],
            email=register_data["email"],
            password=register_data["password"]
        )

        expect(
            page.get_by_text("Подтвердите свою почту")
        ).to_be_visible()

        login_page.open()

        login_page.login(
            register_data["email"],
            register_data["password"]
        )

        expect(page).to_have_url(login_page.home_url)
        expect(
            page.get_by_text("Вы вошли в аккаунт")
        ).to_be_visible()

        # 1. Нажимаем "Все фильмы"
        movies_page.open()

        # 2. Выставляем фильтры
        movies_page.select_city("MSK")
        movies_page.select_genre("Боевик")

        # сортировку можно добавить, если нужна
        # movies_page.select_sort("По рейтингу")

        # 3. Открываем первый фильм из результатов
        movies_page.open_first_movie()

        # 4. Оставляем отзыв
        review_text = "Отличный фильм"

        movie_page.add_review(review_text)

        # 5. Проверяем, что отзыв появился
        expect(
            page.get_by_text(review_text)
        ).to_be_visible()