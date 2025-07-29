import requests

BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/orders'

def test_get_orders_returns_list():
    response = requests.get(BASE_URL)
    assert response.status_code == 200, f"Ожидался код 200, получили {response.status_code}"

    response_json = response.json()

    # Проверяем, что в ответе есть ключ с заказами — например, "orders" или "list"
    # Тут нужно знать точное имя поля в ответе, предположим, что это "orders"
    assert "orders" in response_json, "В ответе нет ключа 'orders'"

    # Проверяем, что 'orders' — это список
    assert isinstance(response_json["orders"], list), "'orders' не является списком"

    # Опционально: если список не пустой, проверить тип элементов
    if response_json["orders"]:
        first_order = response_json["orders"][0]
        assert isinstance(first_order, dict), "Элемент списка заказов не является объектом"
