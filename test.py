from unittest.mock import Mock


# Псевдокод отображающий ваш реальный класс который ходит на сайт гисметео и достает
# текущую температуру в градусах цельсия
class ThermometerServise:
    def get_weather(self, city) -> Int:
        return gismeteo_client.request_weather(city)


gismeteo_mock = Mock(spec=ThermometerServise)
gismeteo_mock.get_weather.return_value = 100


# Мок для изоляции теста
def test_fetch_data():
    # Тестируемый код используем ваш сервис но передаем в него данные их мока
    temperature = gismeteo_mock.get_weather("Moscow")

    result = my_service.check_temperature(temperature)
    assert result == True