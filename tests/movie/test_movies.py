import pytest
import requests
from requests.utils import get_unicode_from_response

from custom_requester.custom_requester import CustomRequester



def test_get_movies(movie_manager):
    """Проверяем получение афиши по параметрам"""
    response = movie_manager.movies_api.get_movies(params={
    "page": 1,
    "genreId": 10,
    "pageSize": 1,
    "minPrice": 1,
    "maxPrice": 9999,
    "published": True,
    }).json()

    assert response["movies"][0]["genre"]["name"] == "Военный", \
    f"Ожидали получить 'Военный' - получили {response["movies"][0]["genre"]["name"]}"
    assert response["movies"][0]["id"] == 266

def test_create_and_get_movie(movie_manager, test_movie, authenticated_admin):
    """Проверяем создание фильма"""
    #Заходим под SUPER_ADMIN
    authenticated_admin

    #Создаем фильм
    response_data = movie_manager.movies_api.create_movie(test_movie).json()

    #Проверяем полученные данные
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

    #Получаем наш фильм по id по GET
    get_response = movie_manager.movies_api.get_movie_by_id(response_data["id"]).json()

    #Проверяем теперь, что получили наш созданный фильм
    assert get_response["id"] == response_data["id"]
    assert get_response["name"] == test_movie["name"]
    assert get_response["imageUrl"] == test_movie["imageUrl"]
    assert get_response["price"] == test_movie["price"]
    assert get_response["description"] == test_movie["description"]
    assert get_response["location"] == test_movie["location"]
    assert get_response["published"] == test_movie["published"]
    assert get_response["genreId"] == test_movie["genreId"]


def test_get_movie_unvalid_id(movie_manager):
    """Оброащение по невалидвную id"""
    #Обращаемся к несущестующему id
    with pytest.raises(ValueError):
        movie_manager.movies_api.get_movie_by_id(-1)

def test_delete_movie(movie_manager, authenticated_admin, test_movie):
    """Удаление фильма"""
    #Логинимся под админом
    authenticated_admin

    #Создаем тестовый фильм и забираем id фильма
    create_response = movie_manager.movies_api.create_movie(test_movie).json()
    movie_id = create_response["id"]

    #Удаляем фильм
    delete_response = movie_manager.movies_api.delete_movie_by_id(movie_id).json()

    #Проверяем, что есть поле reviews
    assert "reviews" in delete_response
    assert isinstance(delete_response["reviews"], list)
    assert len(delete_response["reviews"]) == 0

    #Проверям данные с созданным фильмом и удаленным
    assert delete_response["id"] == create_response["id"]
    assert delete_response["name"] == create_response["name"]
    assert delete_response["price"] == create_response["price"]
    assert delete_response["imageUrl"] == create_response["imageUrl"]
    assert delete_response["location"] == create_response["location"]
    assert delete_response["published"] == create_response["published"]
    assert delete_response["genreId"] == create_response["genreId"]

    #Убеждаемся, что фильм реально удален
    with pytest.raises(ValueError):
        movie_manager.movies_api.get_movie_by_id(movie_id)

def test_edit_movie(movie_manager, authenticated_admin, test_movie):
    """Проверяем изменение фильма"""
    #Логинимся под админом
    authenticated_admin

    #Создаем тест фильм и забираем id
    create_response = movie_manager.movies_api.create_movie(test_movie).json()
    movie_id = create_response["id"]

    #Подготовим данные для изменения
    movie_data = {
        "price": 1337
    }

    #Отправляем запрос на изменение
    edit_response = movie_manager.movies_api.edit_movie_by_id(movie_id,movie_data).json()

    #Проверяем, что данные изменились
    assert edit_response["price"] == movie_data["price"]


def test_edit_movie_negative_price(movie_manager, test_movie, authenticated_admin):
    """Проверяем изменение фильма на негативную цену"""
    #Логинимся под админом
    authenticated_admin

    #Создаем тест фильм и забираем id
    create_response = movie_manager.movies_api.create_movie(test_movie).json()
    movie_id = create_response["id"]

    #Подготовим данные для изменения
    movie_data = {
        "price": -1337
    }

    #Отправляем запрос на изменение
    edit_response = movie_manager.movies_api.edit_movie_by_id(movie_id,movie_data, expected_status=400).json()
    assert edit_response["error"] == "Bad Request"
    assert edit_response["statusCode"] == 400
    assert edit_response["message"][0] == "price must not be less than 1"

def test_edit_movie_boundary_price(movie_manager,test_movie,authenticated_admin):
    """Проверяем граничное значение меньше 1"""
    #Логинимся под админом
    authenticated_admin

    #Создаем тест фильм и забираем id
    create_response = movie_manager.movies_api.create_movie(test_movie).json()
    movie_id = create_response["id"]

    #Подготовим данные для изменения
    movie_data = {
        "price": 0.99
    }

    #Отправляем запрос на изменение
    edit_response = movie_manager.movies_api.edit_movie_by_id(movie_id,movie_data, expected_status=400).json()
    assert edit_response["error"] == "Bad Request"
    assert edit_response["statusCode"] == 400
    assert edit_response["message"][0] == "price must not be less than 1"

def test_edit_movie_rounding_movie(movie_manager,test_movie,authenticated_admin):
    #Логинимся под админом
    authenticated_admin

    #Создаем тест фильм и забираем id
    create_response = movie_manager.movies_api.create_movie(test_movie).json()
    movie_id = create_response["id"]

    #Подготовим данные для изменения
    movie_data = {
        "price": 125.51
    }

    #Отправляем запрос на изменение
    edit_response = movie_manager.movies_api.edit_movie_by_id(movie_id,movie_data, expected_status=200).json()
    assert edit_response["price"] == 125, \
    f"Ожидали получить 125 - получили {edit_response['price']}"