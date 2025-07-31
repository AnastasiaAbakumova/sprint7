import requests
import random
import string
import allure
from app.urls import COURIER_REGISTER, COURIER_LOGIN


def generate_random_string(length=10):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


@allure.step("Регистрация курьера: login={login}, firstName={first_name}")
def register_courier(login, password, first_name):
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    return requests.post(COURIER_REGISTER, data=payload)


@allure.step("Авторизация курьера: login={login}")
def login_courier(login, password):
    payload = {"login": login, "password": password}
    return requests.post(COURIER_LOGIN, data=payload)


def register_new_courier_and_return_login_password():
    login = generate_random_string()
    password = generate_random_string()
    first_name = generate_random_string()

    response = register_courier(login, password, first_name)
    if response.status_code == 201:
        return login, password
    return None, None


def get_base_order_data():
    return {
        "firstName": generate_random_string(),
        "lastName": generate_random_string(),
        "address": "ул. Тестовая, д.1",
        "metroStation": 4,
        "phone": "+79999999999",
        "rentTime": 1,
        "deliveryDate": "2025-08-01",
        "comment": "Тестовый заказ"
    }