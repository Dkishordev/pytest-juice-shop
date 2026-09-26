import pytest
from pages.login_page import LoginPage


@pytest.mark.ui
def test_valid_credentials_log_the_user_in(page, test_user):
    login = LoginPage(page).open()
    login.login(test_user["email"], test_user["password"])
    assert login.is_logged_in(), "Valid credentials did not result in a logged-in session"
    assert "/login" not in login.current_url(), "User was not redirected away from the login page"


@pytest.mark.ui
def test_invalid_credentials_keep_user_on_login_page(page, test_user):
    login = LoginPage(page).open()
    login.login(test_user["email"], "wrong-password-123")
    assert not login.is_logged_in(), "Login should not succeed with an incorrect password"
    assert "/login" in login.current_url(), "User was navigated away from login despite bad credentials"


@pytest.mark.ui
def test_logout_clears_local_storage_token(logged_in_page):
    from pages.base_page import BasePage
    base = BasePage(logged_in_page)
    assert base.get_local_storage_token() is not None, "Fixture did not result in a logged-in session"
    logged_in_page.goto(f"{base.base_url}/#/")
    logged_in_page.locator("#navbarAccount, button[aria-label='Account']").first.click()
    logged_in_page.locator("#navbarLogoutButton, button:has-text('Logout')").first.click()
    logged_in_page.wait_for_timeout(500)
    assert base.get_local_storage_token() is None, "Auth token remained in local storage after logout"
