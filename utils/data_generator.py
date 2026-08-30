import random
from datetime import timedelta
from faker import Faker
import datetime

faker = Faker()

class DataGenerator:

    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))
        return f"kek{random_string}@gmail.com"

    @staticmethod
    def generate_firstname():
        return faker.first_name()

    @staticmethod
    def generate_lastname():
        return faker.last_name()

    @staticmethod
    def generate_total_price():
        return random.randint(100, 5000)

    @staticmethod
    def generate_deposit_paid():
        return faker.boolean()

    @staticmethod
    def generate_checkin_date():
        return faker.date_between(start_date='today', end_date='+30d')

    @staticmethod
    def generate_checkout_date(checkin_date):
        return checkin_date + timedelta(days=random.randint(1, 14))

    @staticmethod
    def generate_additional_needs():
        options = ["Breakfast", "Lunch", "Dinner", "Late checkout", "Extra bed", ""]
        return random.choice(options)

    @staticmethod
    def generate_password():
        """
        Генерирует пароль, соответствующий требованиям:
        - Длина от 8 до 20 символов
        - Только латиница (a-zA-Z)
        - Минимум 1 заглавная буква
        - Минимум 1 строчная буква
        - Минимум 1 цифра
        - Минимум 1 спецсимвол из разрешенного списка
        """
        # Определяем наборы символов (ТОЛЬКО ЛАТИНИЦА!)
        uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        lowercase = 'abcdefghijklmnopqrstuvwxyz'
        digits = '0123456789'
        special = '?@#$%^&*_-+()[]{}><\\/|"\'.,:;'

        # Гарантируем наличие всех обязательных типов символов
        password_chars = [
            random.choice(uppercase),
            random.choice(lowercase),
            random.choice(digits),
            random.choice(special),
        ]

        # Добавляем случайные символы до нужной длины
        all_chars = uppercase + lowercase + digits + special
        remaining_length = random.randint(4, 16)
        password_chars.extend(random.choices(all_chars, k=remaining_length))

        random.shuffle(password_chars)
        return ''.join(password_chars)

    @staticmethod
    def generate_random_name():
        return faker.name()

    @staticmethod
    def generate_id_db():
        return faker.random_int(min=1, max=100000)

    @staticmethod
    def generate_fake_price():
        return faker.random_int(100, 1000)

    @staticmethod
    def generate_description():
        return faker.text(100)

    @staticmethod
    def generate_name_movie():
        return faker.sentence(nb_words=3)

    @staticmethod
    def generate_url():
        return faker.image_url()

    @staticmethod
    def generate_locations():
        return faker.random_element(["MSK", "SPB"])

    @staticmethod
    def generate_id():
        return faker.random_int(5,10)

    @staticmethod
    def generate_boolean():
        return faker.boolean()

    @staticmethod
    def generate_float():
        return faker.pyfloat()

    @staticmethod
    def generate_user_data() -> dict:
        """Генерирует данные для тестового пользователя"""
        from uuid import uuid4

        return {
            'id': f'{uuid4()}',  # генерируем UUID как строку
            'email': DataGenerator.generate_random_email(),
            'full_name': DataGenerator.generate_random_name(),
            'password': DataGenerator.generate_password(),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'verified': False,
            'banned': False,
            'roles': '{USER}'
        }

    @staticmethod
    def generate_movie_data() -> dict:
        """Генерирует данные для тестового фильма"""
        from uuid import uuid4

        return {
            'id': DataGenerator.generate_id_db(),
            'name': DataGenerator.generate_name_movie(),
            'price': DataGenerator.generate_fake_price(),
            'description': DataGenerator.generate_description(),
            'image_url': DataGenerator.generate_url(),
            'location': DataGenerator.generate_locations(),
            'published': DataGenerator.generate_boolean(),
            'rating': DataGenerator.generate_float(),
            'genre_id': DataGenerator.generate_id(),
            'created_at': datetime.datetime.now()
        }

    @staticmethod
    def generate_random_int(min=0):
        return faker.random_int(0, 450)