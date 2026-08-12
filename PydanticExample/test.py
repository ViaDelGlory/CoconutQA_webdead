from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Optional
from venv import logger
from enum import Enum
import pytest

class Product(BaseModel):
    name: str
    price: float
    in_stock: bool

data = {
    "name": "Slava",
    "price": 1337.13,
    "in_stock": False
}
x = Product(**data)
print(x)

json_x = x.model_dump_json()
print(json_x)

new_x = Product.model_validate_json(json_x)
print(new_x)