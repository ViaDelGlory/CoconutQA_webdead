import random
from datetime import timedelta
from faker import Faker

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
        - Минимум 1 буква (латиница или кириллица)
        - Минимум 1 цифра
        - Разрешенные спецсимволы: ?@#$%^&*_-+()[]{}><\\/|"'.,:;
        """
        # Определяем наборы символов
        letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        digits = '0123456789'
        special = '?@#$%^&*_-+()[]{}><\\/|"\'.,:;'

        # Гарантируем наличие хотя бы одной буквы, цифры и спецсимвола
        password_chars = [
            random.choice(letters),  # минимум 1 буква
            random.choice(digits),  # минимум 1 цифра
            random.choice(special),  # минимум 1 спецсимвол
        ]

        # Добавляем случайные символы до нужной длины (от 8 до 20)
        all_chars = letters + digits + special
        remaining_length = random.randint(5, 17)  # 8-20 минус 3 обязательных
        password_chars.extend(random.choices(all_chars, k=remaining_length))

        # Перемешиваем для случайного порядка
        random.shuffle(password_chars)

        return ''.join(password_chars)

    @staticmethod
    def generate_random_name():
        return faker.name()

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
