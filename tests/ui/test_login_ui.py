import pytest
from pages.login_page import LoginPage
from utils.helpers import random_email
from playwright.sync_api import expect


@pytest.mark.ui
def test_ui05_valid_credentials_log_the_user_in(page, test_user):
    login = LoginPage(page).open()
    login.login(test_user["email"], test_user["password"])
    assert login.is_logged_in(), "Valid credentials did not result in a logged-in session"
    assert "/login" not in login.current_url(), "User was not redirected away from the login page"


@pytest.mark.ui
def test_ui06_invalid_credentials_keep_user_on_login_page(page, test_user):
    login = LoginPage(page).open()
    login.login(test_user["email"], "wrong-password-123")
    assert not login.is_logged_in(), "Login should not succeed with an incorrect password"
    assert "/login" in login.current_url(), "User was navigated away from login despite bad credentials"


@pytest.mark.ui
def test_ui07_login_nonexistent_user(page):
    login = LoginPage(page).open()
    login.login(random_email(), "Passw0rd!123")
    expect(login.err_message).to_contain_text("Invalid email or password")


@pytest.mark.ui
def test_ui08_login_button_disabled_when_empty(page):
    login = LoginPage(page).open()
    expect(login.loginbutton).to_be_disabled()


@pytest.mark.ui
def test_ui09_logout_clears_local_storage_token(logged_in_page):
    from pages.base_page import BasePage
    base = BasePage(logged_in_page)
    assert base.get_local_storage_token() is not None, "Fixture did not result in a logged-in session"
    logged_in_page.goto(f"{base.base_url}/#/")
    logged_in_page.locator("#navbarAccount, button[aria-label='Account']").first.click()
    logged_in_page.locator("#navbarLogoutButton, button:has-text('Logout')").first.click()
    logged_in_page.wait_for_timeout(500)
    assert base.get_local_storage_token() is None, "Auth token remained in local storage after logout"
