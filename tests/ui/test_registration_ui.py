import pytest
import re
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from utils.helpers import random_email, random_password
from playwright.sync_api import expect


@pytest.mark.ui
def test_ui01_register_new_user(page):
    email = random_email()
    password = random_password()
    RegisterPage(page).open().register(email, password)
    page.wait_for_timeout(500)
    expect(page).to_have_url(re.compile(r"#/login"))


@pytest.mark.ui
def test_ui02_register_password_mismatch(page):
    reg = RegisterPage(page).open()
    reg.email.fill(random_email())
    reg.password.fill("Passw0rd!123")
    reg.repeat.fill("Different!456")
    reg.repeat.press("Tab")
    expect(reg.errors.first).to_be_visible()
    expect(reg.submit).to_be_disabled()


@pytest.mark.ui
def test_ui03_register_invalid_email(page):
    reg = RegisterPage(page).open()
    reg.email.fill("not-an-email")
    reg.email.press("Tab")
    expect(reg.errors.first).to_be_visible()
    expect(reg.submit).to_be_disabled() 

@pytest.mark.smoke
@pytest.mark.ui
def test_ui04_registered_user_can_immediately_log_in(page):
    email = random_email()
    password = random_password()
    RegisterPage(page).open().register(email, password)
    page.wait_for_timeout(500)
    login = LoginPage(page).open()
    login.login(email, password)
    assert login.is_logged_in(), "Newly registered user could not log in with the same credentials"