from typing import Optional, Union

def multiply(a: int, b: int) -> int:
    return a * b

y = multiply(1, 2)
print(y)

#x = multiply("321", "123")
#print(x)

"""
def sum_numbers(numbers: list[int]) -> int:
    return sum(numbers)

z = sum_numbers([1,2,3])
print(z)

q = sum_numbers(["one", "two", "three"])
print(q)
"""
"""
def find_user(user_id: int) -> Optional[str]:
    if user_id == 1:
        return "Пользователь найден"
    return None

x = print(find_user(1))
w = print(find_user(3))
"""
"""
def process_input(value: Union[str, int]) -> str:
    return f"Ты передал: {value}"

o = process_input(1)
print(o)

p = process_input("Xyu")
print(p)
"""

class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def greet(self) -> str:
        return f"Привет, меня зовут {self.name}!"

user1 = User("Артем", 25)
print(user1.greet())