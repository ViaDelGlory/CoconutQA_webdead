import pytest
import requests
from clients.auth_api import AuthApi
from clients.movie_manager import MoviesManager
from custom_requester.custom_requester import CustomRequester
from config.base_urls import AUTH_BASE_URL
from data.auth.register_data import get_register_payload
from clients.api_manager import ApiManager
from data.movies.movies_data import get_movie_data
from entities.user import User
from resoures.user_creds import SuperAdminCreds
from constants.roles import Roles
from utils.data_generator import DataGenerator
from models.base_models import TestUser

@pytest.fixture(scope="session")
def session():
    return requests.Session()

@pytest.fixture()
def registration_user_data(test_user: TestUser) -> TestUser:
    return test_user

@pytest.fixture
def test_user_original():
    random_password = DataGenerator.generate_password()

    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": [Roles.USER.value]
    }

@pytest.fixture
def test_user() -> TestUser:
    random_password = DataGenerator.generate_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value]
    )


@pytest.fixture(scope="session")
def test_user_2() -> TestUser:
    random_password = DataGenerator.generate_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value]
    )

@pytest.fixture(scope="session")
def test_user_3() -> TestUser:
    random_password = DataGenerator.generate_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value]
    )

@pytest.fixture(scope="session")
def test_user_4() -> TestUser:
    random_password = DataGenerator.generate_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value]
    )

@pytest.fixture
def login_data(registration_user_data):
    return {
        "email": registration_user_data.email,
        "password": registration_user_data.password
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

@pytest.fixture(scope="session")
def movie_manager(session):
    return MoviesManager(session)

@pytest.fixture(scope="function")
def test_movie():
    return get_movie_data()

@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture(scope="function")
def creation_user_data(test_user: TestUser) -> TestUser:
    return test_user.model_copy(
        update={
            "verified": True,
            "banned": False,
        }
    )

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.USER.value],
        new_session)

    super_admin.api.user_api.create_user(creation_user_data.model_dump(mode="json"))
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture
def admin_user(user_session, super_admin, creation_user_data: TestUser):
    new_session = user_session()

    creation_user_data = creation_user_data.model_copy(
        update={
            "roles": [Roles.ADMIN]
        }
    )

    admin_user = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.ADMIN.value],
        new_session
    )

    super_admin.api.user_api.create_user(
        creation_user_data.model_dump(mode="json")
    )

    admin_user.api.auth_api.authenticate(admin_user.creds)

    return admin_user

#Прокси фикстура для параметризации
@pytest.fixture
def user(request):
    return request.getfixturevalue(request.param)