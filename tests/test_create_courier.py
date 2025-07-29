import allure
from app.courier import register_new_courier_and_return_login_password
import requests
import random
import string

BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/courier'
LOGIN_URL = 'https://qa-scooter.praktikum-services.ru/api/v1/courier/login'


def generate_random_string(length=10):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


@allure.title("Успешное создание курьера и вход")
def test_create_courier_success():
    creds = register_new_courier_and_return_login_password()
    assert len(creds) == 3, "Курьер не создан — список пустой или неполный"

    payload = {"login": creds[0], "password": creds[1]}
    response = requests.post(LOGIN_URL, data=payload)
    assert response.status_code == 200, "Не удалось залогиниться после создания курьера"
    assert "id" in response.json(), "В ответе нет ID курьера"


@allure.title("Запрет создания курьера с дублирующимся логином")
def test_cannot_create_duplicate_courier():
    login = generate_random_string()
    password = generate_random_string()
    first_name = generate_random_string()

    payload = {"login": login, "password": password, "firstName": first_name}

    response1 = requests.post(BASE_URL, data=payload)
    assert response1.status_code == 201, f"Ожидали 201, получили {response1.status_code}"

    response2 = requests.post(BASE_URL, data=payload)
    assert response2.status_code == 409, f"Ожидали 409, получили {response2.status_code}"


@allure.title("Создание курьера с отсутствующими обязательными полями")
def test_create_courier_missing_required_fields():
    payload = {"password": generate_random_string(), "firstName": generate_random_string()}
    response = requests.post(BASE_URL, data=payload)
    assert response.status_code == 400, "Ожидали 400 при отсутствии login"

    payload = {"login": generate_random_string(), "firstName": generate_random_string()}
    response = requests.post(BASE_URL, data=payload)
    assert response.status_code == 400, "Ожидали 400 при отсутствии password"

    payload = {"login": generate_random_string(), "password": generate_random_string()}
    response = requests.post(BASE_URL, data=payload)
    assert response.status_code == 201, "Ожидали успешное создание без firstName"


@allure.title("Проверка кода ответа при регистрации курьера")
def test_register_courier_response_code():
    payload = {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string()
    }
    response = requests.post(BASE_URL, data=payload)
    assert response.status_code == 201, f"Ожидали 201, получили {response.status_code}"


@allure.title("Проверка ответа ok True при регистрации")
def test_register_courier_returns_ok_true():
    payload = {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string()
    }
    response = requests.post(BASE_URL, data=payload)
    assert response.status_code == 201, f"Ожидали 201, получили {response.status_code}"
    assert response.json() == {"ok": True}, f"Ожидали 'ok': True, получили {response.json()}"


@allure.title("Проверка 400 при отсутствии обязательных полей")
def test_register_courier_missing_required_fields_loop():
    base_payload = {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string()
    }
    required_fields = ["login", "password"]

    for field in required_fields:
        payload = base_payload.copy()
        payload.pop(field)
        response = requests.post(BASE_URL, data=payload)
        assert response.status_code == 400, f"При отсутствии '{field}' ожидали 400, получили {response.status_code}"


@allure.title("Запрет регистрации с дублирующим логином")
def test_register_courier_duplicate_login():
    login = generate_random_string()
    password1 = generate_random_string()
    first_name1 = generate_random_string()

    payload1 = {"login": login, "password": password1, "firstName": first_name1}
    response1 = requests.post(BASE_URL, data=payload1)
    assert response1.status_code == 201, f"Ожидали 201 при создании, получили {response1.status_code}"

    password2 = generate_random_string()
    first_name2 = generate_random_string()

    payload2 = {"login": login, "password": password2, "firstName": first_name2}
    response2 = requests.post(BASE_URL, data=payload2)
    assert response2.status_code in [400, 409], f"Ожидали 400 или 409 при дублировании, получили {response2.status_code}"
