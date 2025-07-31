import requests
import allure
from app.urls import ORDER_CREATE

class TestGetOrders:

    @allure.title("Сервер возвращает статус 200 при запросе списка заказов")
    def test_get_orders_status_code(self):
        with allure.step("Отправляем GET запрос для получения списка заказов"):
            response = requests.get(ORDER_CREATE)
        with allure.step(f"Проверяем, что статус код равен 200, а получен {response.status_code}"):
            assert response.status_code == 200, f"Ожидали код 200, получили {response.status_code}"

    @allure.title("В ответе присутствует ключ 'orders'")
    def test_get_orders_contains_orders_key(self):
        response = requests.get(ORDER_CREATE)
        response_json = response.json()
        with allure.step("Проверяем, что в ответе есть ключ 'orders'"):
            assert "orders" in response_json, "В ответе нет ключа 'orders'"

    @allure.title("Поле 'orders' является списком")
    def test_get_orders_orders_is_list(self):
        response = requests.get(ORDER_CREATE)
        response_json = response.json()
        with allure.step("Проверяем, что 'orders' — это список"):
            assert isinstance(response_json.get("orders", None), list), "'orders' не список"

    @allure.title("Если список заказов не пустой, первый заказ — словарь")
    def test_get_orders_first_order_is_dict(self):
        response = requests.get(ORDER_CREATE)
        response_json = response.json()
        orders = response_json.get("orders", [])
        if orders:
            with allure.step("Проверяем, что первый заказ — это словарь с данными"):
                first_order = orders[0]
                assert isinstance(first_order, dict), "Первый заказ не является словарём с данными"
        else:
            with allure.step("Список заказов пуст, проверка первого заказа пропущена"):
                pass
