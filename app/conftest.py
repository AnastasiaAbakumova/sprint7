import pytest
from app.helpers import register_new_courier_and_return_login_password

@pytest.fixture
def new_courier():
    login, password = register_new_courier_and_return_login_password()
    assert login is not None, "Не удалось зарегистрировать курьера"
    return login, password
