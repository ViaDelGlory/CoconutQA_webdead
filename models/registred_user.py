from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Optional
from venv import logger
from enum import Enum
import pytest

class Roles(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"

class RegistrationUser(BaseModel):
    email: str = Field(...)
    fullName: str
    password: str = Field(..., min_length= 8)
    passwordRepeat: str
    roles: list[Roles]
    banned: Optional[bool] = None
    verified: Optional[bool] = None

    @field_validator("email")
    @classmethod
    def check_email(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("Email должен содержать @")
        return value

def test_pydantic_model(test_user):
    user = RegistrationUser(**test_user)
    assert user.fullName == test_user["fullName"]
    print(user.model_dump_json(exclude_unset=True))

def test_pydantic_model1(creation_user_data):
    user = RegistrationUser(**creation_user_data)
    assert user.fullName == creation_user_data["fullName"]
    print(user.model_dump_json())

def test_bad_user():
    bad_user = {
        "email": "testmail.com",  # нет @
        "fullName": "Ivan",
        "password": "123",  # меньше 8 символов
        "passwordRepeat": "123",
        "roles": ["USER"]
    }
    with pytest.raises(ValidationError):
        RegistrationUser(**bad_user)