import requests
import allure

BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/orders'

@allure.title("Проверка, что список заказов возвращается корректно")
def test_get_orders_returns_list():
    response = requests.get(BASE_URL)
    # Проверяем, что запрос прошёл успешно и сервер ответил кодом 200
    assert response.status_code == 200, f"Ожидали код 200, получили {response.status_code}"

    response_json = response.json()

    # Проверяем, что в ответе есть ключ 'orders' — там должен быть список заказов
    assert "orders" in response_json, "В ответе нет ключа 'orders'"

    # Проверяем, что 'orders' — это список (массив)
    assert isinstance(response_json["orders"], list), "'orders' не список"

    # Если список заказов не пустой, проверяем, что первый элемент — это словарь с данными заказа
    if response_json["orders"]:
        first_order = response_json["orders"][0]
        assert isinstance(first_order, dict), "Первый заказ не является словарём с данными"
