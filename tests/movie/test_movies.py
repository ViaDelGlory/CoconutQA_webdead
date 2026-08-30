import pytest
import allure
import requests
from requests.utils import get_unicode_from_response

from custom_requester.custom_requester import CustomRequester
from db_models.movies import MovieDBModel


@allure.epic("Movies API")
@allure.feature("Movies Management")
@allure.suite("Movies Tests")
@allure.label("qa_name", "webdead")
class TestMovies:

    @allure.title("Получение фильмов с фильтрацией по параметрам")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверяем получение афиши по параметрам: page, genreId, pageSize, minPrice, maxPrice, published")
    @pytest.mark.smoke
    @pytest.mark.regress
    @pytest.mark.movies
    def test_get_movies(self, movie_manager):
        """Проверяем получение афиши по параметрам"""
        with allure.step("Отправляем GET запрос с параметрами фильтрации"):
            response = movie_manager.movies_api.get_movies(params={
                "page": 1,
                "genreId": 10,
                "pageSize": 1,
                "minPrice": 1,
                "maxPrice": 9999,
                "published": True,
            }).json()

        with allure.step("Проверяем, что жанр фильма - 'Военный'"):
            assert response["movies"][0]["genre"]["name"] == "Военный", \
                f"Ожидали получить 'Военный' - получили {response['movies'][0]['genre']['name']}"

        with allure.step("Проверяем, что id фильма равен 266"):
            assert response["movies"][0]["id"] == 266

    @allure.title("Создание и получение фильма")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверяем создание фильма и последующее получение по id")
    @pytest.mark.smoke
    @pytest.mark.regress
    @pytest.mark.critical
    @pytest.mark.movies
    def test_create_and_get_movie(self, movie_manager, test_movie, authenticated_admin):
        """Проверяем создание фильма"""
        with allure.step("Логинимся под SUPER_ADMIN"):
            authenticated_admin

        with allure.step("Создаем новый фильм через API"):
            response_data = movie_manager.movies_api.create_movie(test_movie).json()

        with allure.step("Проверяем, что фильм создан с корректными данными"):
            assert response_data["id"] > 0, \
                f"Ожидаем, что id будет больше нуля - на самом деле {response_data['id']}"
            assert "id" in response_data, \
                f"Ожидаем получить в JSON 'id'"
            assert isinstance(response_data["id"], int), \
                f"Ожидаем, что 'id' = int, получили - {response_data['id']}"
            assert response_data["name"] == test_movie["name"]
            assert response_data["imageUrl"] == test_movie["imageUrl"]
            assert response_data["price"] == test_movie["price"]
            assert response_data["description"] == test_movie["description"]
            assert response_data["location"] == test_movie["location"]
            assert response_data["published"] == test_movie["published"]
            assert response_data["genreId"] == test_movie["genreId"]

        with allure.step("Получаем созданный фильм по id через GET запрос"):
            get_response = movie_manager.movies_api.get_movie_by_id(response_data["id"]).json()

        with allure.step("Проверяем, что полученный фильм соответствует созданному"):
            assert get_response["id"] == response_data["id"]
            assert get_response["name"] == test_movie["name"]
            assert get_response["imageUrl"] == test_movie["imageUrl"]
            assert get_response["price"] == test_movie["price"]
            assert get_response["description"] == test_movie["description"]
            assert get_response["location"] == test_movie["location"]
            assert get_response["published"] == test_movie["published"]
            assert get_response["genreId"] == test_movie["genreId"]

    @allure.title("Обращение по невалидному id")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description("Проверяем, что при обращении к несуществующему id возвращается ошибка")
    @pytest.mark.regress
    @pytest.mark.negative
    @pytest.mark.movies
    def test_get_movie_unvalid_id(self, movie_manager):
        """Обращение по невалидному id"""
        with allure.step("Обращаемся к несуществующему id (-1)"):
            with pytest.raises(ValueError):
                movie_manager.movies_api.get_movie_by_id(-1)

    @allure.title("Удаление фильма")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверяем удаление фильма и что после удаления он недоступен")
    @pytest.mark.smoke
    @pytest.mark.regress
    @pytest.mark.critical
    @pytest.mark.movies
    def test_delete_movie(self, movie_manager, authenticated_admin, test_movie):
        """Удаление фильма"""
        with allure.step("Логинимся под админом"):
            authenticated_admin

        with allure.step("Создаем тестовый фильм и забираем id"):
            create_response = movie_manager.movies_api.create_movie(test_movie).json()
            movie_id = create_response["id"]

        with allure.step("Удаляем созданный фильм"):
            delete_response = movie_manager.movies_api.delete_movie_by_id(movie_id).json()

        with allure.step("Проверяем, что у удаленного фильма есть поле reviews (пустой список)"):
            assert "reviews" in delete_response
            assert isinstance(delete_response["reviews"], list)
            assert len(delete_response["reviews"]) == 0

        with allure.step("Проверяем, что данные удаленного фильма совпадают с созданным"):
            assert delete_response["id"] == create_response["id"]
            assert delete_response["name"] == create_response["name"]
            assert delete_response["price"] == create_response["price"]
            assert delete_response["imageUrl"] == create_response["imageUrl"]
            assert delete_response["location"] == create_response["location"]
            assert delete_response["published"] == create_response["published"]
            assert delete_response["genreId"] == create_response["genreId"]

        with allure.step("Убеждаемся, что фильм реально удален (GET возвращает 404)"):
            with pytest.raises(ValueError):
                movie_manager.movies_api.get_movie_by_id(movie_id)

    @allure.title("Изменение цены фильма")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверяем изменение цены фильма через PATCH запрос")
    @pytest.mark.regress
    @pytest.mark.movies
    @pytest.mark.critical
    def test_edit_movie(self, movie_manager, authenticated_admin, test_movie):
        """Проверяем изменение фильма"""
        with allure.step("Логинимся под админом"):
            authenticated_admin

        with allure.step("Создаем тестовый фильм и забираем id"):
            create_response = movie_manager.movies_api.create_movie(test_movie).json()
            movie_id = create_response["id"]

        with allure.step("Подготавливаем данные для изменения цены"):
            movie_data = {
                "price": 1337
            }

        with allure.step("Отправляем PATCH запрос на изменение цены"):
            edit_response = movie_manager.movies_api.edit_movie_by_id(movie_id, movie_data).json()

        with allure.step("Проверяем, что цена изменилась на 1337"):
            assert edit_response["price"] == movie_data["price"]

    @allure.title("Изменение фильма с отрицательной ценой")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверяем, что нельзя установить отрицательную цену")
    @pytest.mark.regress
    @pytest.mark.negative
    @pytest.mark.movies
    @pytest.mark.boundary
    def test_edit_movie_negative_price(self, movie_manager, test_movie, super_admin):
        """Проверяем изменение фильма на негативную цену"""
        with allure.step("Создаем тестовый фильм и забираем id"):
            create_response = super_admin.api.movies_api.create_movie(test_movie).json()
            movie_id = create_response["id"]

        with allure.step("Подготавливаем данные с отрицательной ценой (-1337)"):
            movie_data = {
                "price": -1337
            }

        with allure.step("Отправляем PATCH запрос с отрицательной ценой (ожидаем 400)"):
            edit_response = super_admin.api.movies_api.edit_movie_by_id(movie_id, movie_data, expected_status=400).json()

        with allure.step("Проверяем, что сервер вернул ошибку 400"):
            assert edit_response["error"] == "Bad Request"
            assert edit_response["statusCode"] == 400
            assert edit_response["message"][0] == "price must not be less than 1"

    @allure.title("Изменение фильма с граничным значением цены")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверяем, что нельзя установить цену меньше 1 (0.99)")
    @pytest.mark.regress
    @pytest.mark.negative
    @pytest.mark.movies
    @pytest.mark.boundary
    def test_edit_movie_boundary_price(self, movie_manager, test_movie, authenticated_admin):
        """Проверяем граничное значение меньше 1"""
        with allure.step("Логинимся под админом"):
            authenticated_admin

        with allure.step("Создаем тестовый фильм и забираем id"):
            create_response = movie_manager.movies_api.create_movie(test_movie).json()
            movie_id = create_response["id"]

        with allure.step("Подготавливаем данные с ценой 0.99"):
            movie_data = {
                "price": 0.99
            }

        with allure.step("Отправляем PATCH запрос с ценой 0.99 (ожидаем 400)"):
            edit_response = movie_manager.movies_api.edit_movie_by_id(movie_id, movie_data, expected_status=400).json()

        with allure.step("Проверяем, что сервер вернул ошибку 400"):
            assert edit_response["error"] == "Bad Request"
            assert edit_response["statusCode"] == 400
            assert edit_response["message"][0] == "price must not be less than 1"

    @allure.title("Округление цены фильма")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверяем, что цена округляется до целого числа")
    @pytest.mark.regress
    @pytest.mark.movies
    def test_edit_movie_rounding_movie(self, movie_manager, test_movie, authenticated_admin):
        """Проверяем округление цены"""
        with allure.step("Логинимся под админом"):
            authenticated_admin

        with allure.step("Создаем тестовый фильм и забираем id"):
            create_response = movie_manager.movies_api.create_movie(test_movie).json()
            movie_id = create_response["id"]

        with allure.step("Подготавливаем данные с дробной ценой 125.51"):
            movie_data = {
                "price": 125.51
            }

        with allure.step("Отправляем PATCH запрос с дробной ценой"):
            edit_response = movie_manager.movies_api.edit_movie_by_id(movie_id, movie_data, expected_status=200).json()

        with allure.step("Проверяем, что цена округлилась до 125"):
            assert edit_response["price"] == 125, \
                f"Ожидали получить 125 - получили {edit_response['price']}"

    @allure.title("Создание фильма обычным пользователем (должен быть 403)")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверяем, что обычный пользователь не может создать фильм")
    @pytest.mark.regress
    @pytest.mark.movies
    @pytest.mark.security
    @pytest.mark.negative
    def test_get_common_user(self, common_user, test_movie):
        with allure.step("Пытаемся создать фильм под обычным пользователем (ожидаем 403)"):
            common_user.api.movies_api.create_movie(test_movie, expected_status=403)

    @allure.title("Создание фильма администратором")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверяем, что администратор может создать фильм")
    @pytest.mark.smoke
    @pytest.mark.regress
    @pytest.mark.movies
    @pytest.mark.security
    def test_get_admin_user(self, admin_user, test_movie):
        with allure.step("Создаем фильм под администратором"):
            admin_user.api.movies_api.create_movie(test_movie)

    @allure.title("Получение фильмов с различными фильтрами")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Проверяем фильтрацию фильмов по цене, локации и жанру")
    @pytest.mark.regress
    @pytest.mark.movies
    @pytest.mark.parametrize(
        "params",
        [
            {"minPrice": 1, "maxPrice": 1000},
            {"locations": ["MSK"]},
            {"genreId": 7},
        ],
        ids=[
            "price_filter",
            "location_filter",
            "genre_filter"
        ],
    )
    def test_movie_with_parametrize(self, common_user, params):
        """Проверяем получение фильма по разным параметрам"""
        with allure.step(f"Отправляем GET запрос с параметрами: {params}"):
            response = common_user.api.movies_api.get_movies(params=params)

        with allure.step("Получаем список фильмов из ответа"):
            movies = response.json()["movies"]

        with allure.step("Проверяем, что все фильмы соответствуют параметрам фильтрации"):
            for movie in movies:
                if "minPrice" in params:
                    assert movie["price"] >= params["minPrice"]

                if "maxPrice" in params:
                    assert movie["price"] <= params["maxPrice"]

                if "locations" in params:
                    assert movie["location"] in params["locations"]

                if "genreId" in params:
                    assert movie["genreId"] == params["genreId"]

    @allure.title("Удаление фильма под разными пользователями")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверяем доступ к удалению фильмов для разных ролей")
    @pytest.mark.regress
    @pytest.mark.movies
    @pytest.mark.security
    @pytest.mark.parametrize(
        "user, expected_status",
        [
            ("common_user", 403),
            ("admin_user", 403),
            ("super_admin", 200)
        ],
        ids=["CommonUser", "AdminUser", "SuperAdmin"],
        indirect=["user"],
    )
    def test_delete_movie_by_id_diff_user(self, user, test_movie, super_admin, expected_status):
        """Проверяем удаление фильмов под разными пользователями"""
        with allure.step("Создаем тестовый фильм под SUPER_ADMIN"):
            movie_data = super_admin.api.movies_api.create_movie(test_movie).json()
            movie_id = movie_data["id"]

        with allure.step(f"Пытаемся удалить фильм под пользователем с ожидаемым статусом {expected_status}"):
            delete_response = user.api.movies_api.delete_movie_by_id(movie_id, expected_status=expected_status).json()

        if expected_status == 200:
            with allure.step("Проверяем, что фильм действительно удален"):
                user.api.movies_api.get_movie_by_id(movie_id, expected_status=404)
                assert delete_response["id"] == movie_id

    @allure.title("Проверка создания и удаления фильма в БД")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Проверяем данные до создания, после создания и удаления в БД")
    @pytest.mark.regress
    @pytest.mark.movies
    @pytest.mark.db
    @pytest.mark.integration
    def test_delete_movie_from_db(self, db_helper, movie_data_db, super_admin):
        """Проверяем данные до создания, после создания и удаления в БД"""
        with allure.step("Проверяем, что фильма из фикстуры нет в базе"):
            assert db_helper.get_movie_by_id(movie_data_db["id"]) is None, \
                f"Ожидали, что не будет фильма до создания, а он оказался в БД (Удалите фильм!)"

        with allure.step("Создаем фильм в БД"):
            movie = db_helper.create_test_movie(movie_data_db)

        with allure.step("Получаем фильм из БД и сравниваем с тестовыми данными"):
            movie_from_db = db_helper.get_movie_by_id(movie.id)
            movie_dict_db = movie_from_db.to_dict()

            # ФИЛЬТРАЦИЯ: убираем 'created_at' из обоих словарей,
            # так как в БД время сохраняется с меньшей точностью (микросекунды обрезаются)
            movie_data_db_filtered = {k: v for k, v in movie_data_db.items() if k != 'created_at'}
            movie_dict_db_filtered = {k: v for k, v in movie_dict_db.items() if k != 'created_at'}

            assert movie_dict_db_filtered == movie_data_db_filtered, \
                f"Ожидаем, что фильм найдется в базе и он равен тестовому фильму"

        with allure.step("Удаляем фильм через API и проверяем удаление в БД"):
            super_admin.api.movies_api.delete_movie_by_id(movie.id)
            assert db_helper.get_movie_by_id(movie.id) is None, \
                f"Ожидали, что фильм после удаления по API уйдет из БД"