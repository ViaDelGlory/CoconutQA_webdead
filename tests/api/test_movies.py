import requests
from custom_requester.custom_requester import CustomRequester

session = requests.session()
requester = CustomRequester(session=session, base_url="https://api.dev-cinescope.coconutqa.ru")

def test_get_movies():
    """Тестируем запрос фильма по жанру"""
    response = requester.send_request("GET", "/movies", params={
    "page": 1,
    "genreId": 10,
    "pageSize": 1,
    "minPrice": 1,
    "maxPrice": 9999,
    "published": True,
    },
    need_logging=True)

    assert response.status_code == 200, \
    f"Ожидали 200 - получили {response.status_code}"
    json_response = response.json()
    assert json_response["movies"][0]["genre"]["name"] == "Военный"


