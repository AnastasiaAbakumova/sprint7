import pytest
import requests
import random
import string

BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/orders'

def generate_random_string(length=8):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

@pytest.mark.parametrize("color", [
    ["BLACK"],       # только черный
    ["GREY"],        # только серый
    ["BLACK", "GREY"],# оба цвета
    [],              # без цвета
    None             # поле color отсутствует
])
def test_create_order_with_various_colors(color):
    payload = {
        "firstName": generate_random_string(),
        "lastName": generate_random_string(),
        "address": "ул. Тестовая, д.1",
        "metroStation": 4,
        "phone": "+79999999999",
        "rentTime": 1,
        "deliveryDate": "2025-08-01",
        "comment": "Тестовый заказ"
    }

    # Если color не None и не пустой список — добавляем в payload
    if color is not None and color != []:
        payload["color"] = color

    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 201, f"Создание заказа с цветом {color} вернуло {response.status_code}"

    response_json = response.json()
    assert "track" in response_json, "В ответе нет поля track"
    assert isinstance(response_json["track"], int), "Поле track должно быть целым числом"
