from clients.auth_api import AuthApi
from clients.user_api import UserApi
from clients.movies_api import MoviesApi

class ApiManager:
    def __init__(self, session):
        self.session = session
        self.auth_api = AuthApi(session)
        self.user_api = UserApi(session)
        self.movies_api = MoviesApi(session)

    def update_session_headers(self, headers):
        """Обновляет заголовки сессии"""
        self.session.headers.update(headers)

    def close_session(self):
        self.session.close()
