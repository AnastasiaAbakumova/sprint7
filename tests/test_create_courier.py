import allure
import requests
from app.helpers import login_courier, generate_random_string, register_courier
from app.urls import COURIER_REGISTER, COURIER_LOGIN


class TestCourierAuth:

    @allure.title("Курьер может авторизоваться")
    def test_courier_can_login(self):
        login = generate_random_string()
        password = generate_random_string()
        first_name = generate_random_string()

        reg_response = register_courier(login, password, first_name)
        assert reg_response.status_code == 201, "Не удалось зарегистрировать курьера"

        response = login_courier(login, password)
        assert response.status_code == 200
        assert 'id' in response.json()

    @allure.title("Ошибка при авторизации без логина")
    def test_courier_login_missing_login(self):
        response = requests.post(COURIER_LOGIN, data={"password": "any_password"})
        assert response.status_code == 400

    @allure.title("Ошибка при авторизации с неверным логином")
    def test_courier_login_wrong_login(self):
        response = login_courier("wronglogin", "any_password")
        assert response.status_code in [400, 404]

    @allure.title("Ошибка при авторизации с неверным паролем")
    def test_courier_login_wrong_password(self):
        login = generate_random_string()
        password = generate_random_string()
        first_name = generate_random_string()

        reg_response = register_courier(login, password, first_name)
        assert reg_response.status_code == 201, "Не удалось зарегистрировать курьера"

        response = login_courier(login, "wrongpassword")
        assert response.status_code in [400, 404]

    @allure.title("Авторизация несуществующего пользователя")
    def test_login_nonexistent_user(self):
        response = login_courier("nonexistent_user_123456", "some_password")
        assert response.status_code == 404
        msg = response.json().get("message", "").lower()
        assert "учетная запись не найдена" in msg or "not found" in msg

    @allure.title("Успешная авторизация возвращает id")
    def test_successful_login_returns_id(self):
        login = generate_random_string()
        password = generate_random_string()
        first_name = generate_random_string()

        reg_response = register_courier(login, password, first_name)
        assert reg_response.status_code == 201, "Не удалось зарегистрировать курьера"

        login_response = login_courier(login, password)
        assert login_response.status_code == 200
        assert isinstance(login_response.json().get("id"), int)
