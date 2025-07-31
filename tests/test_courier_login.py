import pytest
import requests
import allure
from app.helpers import login_courier, register_new_courier_and_return_login_password
from app.urls import COURIER_LOGIN

class TestCourierAuth:

    @allure.title("Курьер может авторизоваться")
    def test_courier_can_login(self):
        login, password = register_new_courier_and_return_login_password()
        assert login is not None, "Не удалось зарегистрировать курьера"

        response = login_courier(login, password)
        assert response.status_code == 200
        assert 'id' in response.json()

    @allure.title("Ошибка при авторизации без логина")
    def test_courier_login_missing_login(self):
        with allure.step("Отправка запроса на авторизацию без login"):
            response = requests.post(COURIER_LOGIN, data={"password": "any_password"})
        assert response.status_code == 400

    @allure.title("Ошибка при авторизации с неверным логином")
    def test_courier_login_wrong_login(self):
        response = login_courier("wronglogin", "any_password")
        assert response.status_code in [400, 404]

    @allure.title("Ошибка при авторизации с неверным паролем")
    def test_courier_login_wrong_password(self):
        login, password = register_new_courier_and_return_login_password()
        assert login is not None, "Не удалось зарегистрировать курьера"

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
        login, password = register_new_courier_and_return_login_password()
        assert login is not None, "Не удалось зарегистрировать курьера"

        response = login_courier(login, password)
        assert response.status_code == 200
        assert isinstance(response.json().get("id"), int)
