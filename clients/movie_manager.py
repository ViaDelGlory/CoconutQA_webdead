from clients.movies_api import MoviesApi


class MoviesManager:
    def __init__(self, session):
        self.session = session
        self.movies_api = MoviesApi(session)

    def update_session_headers(self, headers):
        """Обновляет заголовки сессии"""
        self.session.headers.update(headers)
