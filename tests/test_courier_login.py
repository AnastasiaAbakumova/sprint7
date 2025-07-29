import requests
import random
import string

BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'

def register_new_courier_and_return_login_password():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f'{BASE_URL}/courier', data=payload)

    if response.status_code == 201:
        return login, password
    return None, None


def test_courier_can_login():
    login, password = register_new_courier_and_return_login_password()
    assert login is not None, "Не удалось зарегистрировать курьера"

    payload = {"login": login, "password": password}
    response = requests.post(f'{BASE_URL}/courier/login', data=payload)

    assert response.status_code == 200
    assert 'id' in response.json()


def test_courier_login_missing_login():
    payload = {"password": "any_password"}
    response = requests.post(f'{BASE_URL}/courier/login', data=payload)
    assert response.status_code == 400


def test_courier_login_wrong_login():
    payload = {"login": "wronglogin", "password": "any_password"}
    response = requests.post(f'{BASE_URL}/courier/login', data=payload)
    assert response.status_code in [400, 404]


def test_courier_login_wrong_password():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    reg_payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    reg_response = requests.post(f'{BASE_URL}/courier', data=reg_payload)
    assert reg_response.status_code == 201

    payload = {"login": login, "password": "wrongpassword"}
    response = requests.post(f'{BASE_URL}/courier/login', data=payload)
    assert response.status_code in [400, 404]


def test_login_nonexistent_user():
    payload = {"login": "nonexistent_user_123456", "password": "some_password"}
    response = requests.post(f'{BASE_URL}/courier/login', data=payload)
    assert response.status_code == 404

    json_response = response.json()
    assert "message" in json_response
    msg = json_response["message"].lower()
    assert "учетная запись не найдена" in msg or "not found" in msg


def test_successful_login_returns_id():
    def generate_random_string(length=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

    login = generate_random_string()
    password = generate_random_string()
    first_name = generate_random_string()

    reg_payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    reg_response = requests.post(f'{BASE_URL}/courier', data=reg_payload)
    assert reg_response.status_code == 201

    payload = {"login": login, "password": password}
    login_response = requests.post(f'{BASE_URL}/courier/login', data=payload)
    assert login_response.status_code == 200

    json_response = login_response.json()
    assert "id" in json_response
    assert isinstance(json_response["id"], int)
