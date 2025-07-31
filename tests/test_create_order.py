import pytest
import requests
import allure
from app.urls import ORDER_CREATE
from app.helpers import generate_random_string, get_base_order_data

@allure.step("Отправка запроса на создание заказа")
def send_create_order_request(payload):
    return requests.post(ORDER_CREATE, json=payload)

class TestOrderCreation:

    @allure.title("Создание заказа с разными вариантами цвета")
    @pytest.mark.parametrize("color", [
        ["BLACK"],         # только черный
        ["GREY"],          # только серый
        ["BLACK", "GREY"], # оба цвета
        []                 # без цвета (пустой список)
    ])
    def test_create_order_with_color_field(self, color):
        payload = get_base_order_data()
        payload["color"] = color

        with allure.step(f"Создаем заказ с цветом: {color}"):
            response = send_create_order_request(payload)

        with allure.step(f"Проверяем статус код ответа: {response.status_code}"):
            assert response.status_code == 201, f"Создание заказа с цветом {color} вернуло {response.status_code}"

        with allure.step("Проверяем, что в ответе есть поле 'track' и оно целочисленное"):
            response_json = response.json()
            assert "track" in response_json, "В ответе нет поля track"
            assert isinstance(response_json["track"], int), "Поле track должно быть целым числом"

    @allure.title("Создание заказа без поля color")
    def test_create_order_without_color_field(self):
        payload = get_base_order_data()

        with allure.step("Создаем заказ без поля color"):
            response = send_create_order_request(payload)

        with allure.step(f"Проверяем статус код ответа: {response.status_code}"):
            assert response.status_code == 201, f"Создание заказа без поля color вернуло {response.status_code}"

        with allure.step("Проверяем, что в ответе есть поле 'track' и оно целочисленное"):
            response_json = response.json()
            assert "track" in response_json, "В ответе нет поля track"
            assert isinstance(response_json["track"], int), "Поле track должно быть целым числом"
