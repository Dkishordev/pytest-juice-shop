import pytest
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from utils.helpers import random_email, random_password


@pytest.mark.ui
def test_successful_registration_redirects_to_login(page):
    reg = RegisterPage(page).open()
    reg.register(random_email(), random_password())
    page.wait_for_timeout(500)
    assert "/login" in page.url, "Successful registration did not redirect to the login page"


@pytest.mark.ui
def test_mismatched_passwords_show_validation_error(page):
    reg = RegisterPage(page).open()
    email = random_email()
    reg.page.fill(reg.EMAIL_INPUT, email)
    reg.page.fill(reg.PASSWORD_INPUT, "Password123!")
    reg.page.fill(reg.REPEAT_PASSWORD_INPUT, "DifferentPassword456!")
    reg.page.get_by_text("Security Question").click()
    reg.page.get_by_role("listbox", name="Selection list for the").click()
    reg.page.fill(reg.SECURITY_ANSWER_INPUT, "Blue")
    reg.page.click(reg.REGISTER_BUTTON)
    reg.page.wait_for_timeout(500)
    assert "/login" not in reg.page.url, "Registration proceeded despite mismatched passwords"


@pytest.mark.ui
def test_registered_user_can_immediately_log_in(page):
    email = random_email()
    password = random_password()
    RegisterPage(page).open().register(email, password)
    page.wait_for_timeout(500)
    login = LoginPage(page).open()
    login.login(email, password)
    assert login.is_logged_in(), "Newly registered user could not log in with the same credentials"
 