from tokenize import endpats

from custom_requester.custom_requester import CustomRequester
from config.base_urls import MOVIES_URL

# clients/movies_api.py
MOVIES = "/movies"

class MoviesApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=MOVIES_URL)

    # Получение списка фильмов
    def get_movies(self, expected_status=200, params = None, **kwargs):
        #Наследуем метод CustomRequest - .send_request
        return self.send_request(
            method="GET",
            endpoint=MOVIES,
            expected_status=expected_status,
            params = params,
            **kwargs
        )

    #Метод для создания фильма / Только SUPER_ADMIN
    def create_movie(self, movie_data, expected_status=201, **kwargs):
        return self.send_request(
            method="POST",
            endpoint=MOVIES,
            data=movie_data,
            expected_status=expected_status,
            **kwargs
        )

    #Получение фильма по id
    def get_movie_by_id(self, movie_id, expected_status=200, **kwargs):
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES}/{movie_id}",
            expected_status=expected_status,
            **kwargs
        )

    #Удаление фильма по id / ROLE: SUPER_ADMIN
    def delete_movie_by_id(self, movie_id, expected_status=200, **kwargs):
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES}/{movie_id}",
            expected_status=expected_status,
            **kwargs
        )
    #Редактирование фильма по id/ ROLE: SUPER_ADMIN
    def edit_movie_by_id(self, movie_id, movie_data, expected_status=200, **kwargs):
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES}/{movie_id}",
            expected_status=expected_status,
            data=movie_data
        )