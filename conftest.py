import pytest
from playwright.sync_api import sync_playwright

from config.settings import settings
from api.api_client import APIClient
from db.database import Database
from utils.helpers import random_email, random_password


# Browser

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as playwright:
        browser_type = getattr(playwright, settings.BROWSER)

        browser = browser_type.launch(
            headless=settings.HEADLESS
        )

        yield browser

        browser.close()


@pytest.fixture
def page(browser):
    context = browser.new_context(
        base_url=settings.BASE_URL
    )

    context.set_default_timeout(
        settings.DEFAULT_TIMEOUT_MS
    )

    page = context.new_page()

    yield page

    context.close()


# Database

@pytest.fixture(scope="session")
def database():
    return Database()

@pytest.fixture
def api_client():
    return APIClient()


# Test user

@pytest.fixture
def test_user():
    email = random_email()
    password = random_password()

    client = APIClient()
    response = client.register(email, password)

    assert response.status_code in (200, 201), (
        f"Failed to create test user: {response.text}"
    )
    body = response.json()

    return {
        "id": body["data"]["id"],
        "email": email,
        "password": password
    }


# Logged-in API client

@pytest.fixture
def authenticated_api_client(test_user):
    client = APIClient()

    response = client.login(
        test_user["email"],
        test_user["password"]
    )

    assert response.status_code == 200

    return client


# Logged-in browser page

@pytest.fixture
def logged_in_page(page, test_user):
    from pages.login_page import LoginPage

    login_page = LoginPage(page)

    login_page.open().login(
        test_user["email"],
        test_user["password"]
    )

    return page
