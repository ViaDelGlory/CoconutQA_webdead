# clients/user_api.py
from custom_requester.custom_requester import CustomRequester
from config.base_urls import USER_BASE_URL

class UserApi(CustomRequester):

    def __init__(self, session):
        self.session = session
        super().__init__(session, USER_BASE_URL)

    def get_my_info(self, expected_status=200):
        """Получение информации о текущем пользователе (me)"""
        return self.send_request("GET", "user/me", expected_status=expected_status)

    def get_user(self, user_locator, expected_status=200):
        """Получение пользователя по ID или email"""
        return self.send_request("GET",
                                 f"user/{user_locator}",
                                 expected_status=expected_status)

    def get_user_info(self, user_id, expected_status=200):
        """Алиас для get_user (для обратной совместимости)"""
        return self.get_user(user_id, expected_status)

    def create_user(self, user_data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint="user",
            data=user_data,
            expected_status=expected_status
        )

    def delete_user(self, user_locator, expected_status=200, **kwargs):
        return self.send_request(
            method="DELETE",
            endpoint=f"user/{user_locator}",
            expected_status=expected_status,
            **kwargs
        )