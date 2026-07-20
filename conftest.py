import pytest
import requests
from clients.auth_api import AuthApi
from custom_requester.custom_requester import CustomRequester
from config.base_urls import AUTH_BASE_URL
from data.auth.register_data import get_register_payload
from clients.api_manager import ApiManager

@pytest.fixture(scope="session")
def session():
    return requests.Session()

@pytest.fixture(scope="session")
def test_user():
    return get_register_payload(None)

@pytest.fixture(scope="session")
def test_user_2():
    return get_register_payload(None)

@pytest.fixture(scope="session")
def test_user_3():
    return get_register_payload(None)

@pytest.fixture(scope="session")
def test_user_4():
    return get_register_payload(None)

@pytest.fixture(scope="session")
def login_data(test_user):
    return {
        "email": test_user["email"],
        "password": test_user["password"]
    }

@pytest.fixture(scope="session")
def login_admin():
    return {
        "email": "api1@gmail.com",
        "password": "asdqwe123Q"
        }

@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session)

@pytest.fixture(scope="function")
def authenticated_user(api_manager, test_user, login_data):
    reg_response = api_manager.auth_api.register_user(test_user).json()
    api_manager.auth_api.authenticate(login_data)
    return reg_response

@pytest.fixture(scope="session")
def custom_requester(session):
    return CustomRequester(session)

@pytest.fixture(scope="function")
def authenticated_admin(api_manager,login_admin):
    response = api_manager.auth_api.authenticate(login_admin)
    return response
