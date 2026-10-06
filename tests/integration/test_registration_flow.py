
import pytest
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from utils.helpers import random_email, random_password


@pytest.mark.integration
def test_int10_ui_registration_creates_a_row_in_the_users_table(page, database):
    email, password = random_email(), random_password()
    RegisterPage(page).open().register(email, password)
    page.wait_for_timeout(500)
    row = database.get_user_by_email(email)
    assert row is not None, "User registered via the UI does not exist in the database"


@pytest.mark.integration
def test_int11_user_registered_via_api_can_log_in_via_ui(page, api_client):
    email, password = random_email(), random_password()
    resp = api_client.register(email, password)
    assert resp.status_code in (200, 201)
    login = LoginPage(page).open()
    login.login(email, password)
    assert login.is_logged_in(), "A user created via the API could not log in through the UI"
