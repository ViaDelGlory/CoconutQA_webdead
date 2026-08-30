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
from sqlalchemy.orm import Session
from db_requester.db_client import get_db_session
from db_requester.db_helpers import DBHelper
import time

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

#Фикстуры для БД

@pytest.fixture(scope="module")
def db_session() -> Session:
    """
    Фикстура, которая создает и возвращает сессию для работы с базой данных
    После завершения теста сессия автоматически закрывается
    """
    db_session = get_db_session()
    yield db_session
    db_session.close()


@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    """
    Фикстура для экземпляра хелпера
    """
    db_helper = DBHelper(db_session)
    return db_helper

@pytest.fixture(scope="function")
def created_test_user(db_helper):
    """
    Фикстура, которая создает тестового пользователя в БД
    и удаляет его после завершения теста
    """
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user
    # Cleanup после теста
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)

@pytest.fixture(scope="function")
def created_test_movie(db_helper):
    """Фикстура, которая создает тестовый фильм в БД"""
    movie = db_helper.create_test_movie(DataGenerator.generate_movie_data())
    return movie

@pytest.fixture(scope="function")
def created_test_movie_with_cleanup(db_helper):
    """Фикстура, которая создает тестовый фильм в БД
    и удаляет его после завершения теста
    """
    movie = db_helper.create_test_movie(DataGenerator.generate_movie_data())
    #Очистка
    if db_helper.get_movie_by_id(movie.id):
        db_helper.delete_movie(movie)

@pytest.fixture(scope="function")
def movie_data_db():
    return DataGenerator.generate_movie_data()

@pytest.fixture #была добавлена в файл conftest.py
def delay_between_retries():
    time.sleep(2)  # Задержка в 2 секунды\ это не обязательно но
    yield          # нужно понимать что такая возможность имеется