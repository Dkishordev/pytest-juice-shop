
from __future__ import annotations
import pytest
from playwright.sync_api import sync_playwright, Browser, Page

from config.settings import settings
from api.api_client import APIClient
from db.database import Database
from utils.helpers import random_email, random_password


# browser / page 
@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser_type = getattr(p, settings.BROWSER)
        browser = browser_type.launch(headless=settings.HEADLESS)
        yield browser
        browser.close()


@pytest.fixture
def page(browser: Browser):
    context = browser.new_context(base_url=settings.BASE_URL)
    context.set_default_timeout(settings.DEFAULT_TIMEOUT_MS)
    pg = context.new_page()
    yield pg
    context.close()


# DB clients



@pytest.fixture(scope="session")
def database() -> Database:
    return Database()


@pytest.fixture
def test_user():
    """A fresh, unique user registered via the API for tests that need to log in
    without polluting/relying on any specific pre-seeded account."""
    email = random_email()
    password = random_password()
    client = APIClient()
    resp = client.register(email, password)
    assert resp.status_code in (200, 201), f"Failed to set up test user: {resp.text}"
    return {"email": email, "password": password}


@pytest.fixture
def authenticated_api_client(test_user) -> APIClient:
    client = APIClient()
    resp = client.login(test_user["email"], test_user["password"])
    assert resp.status_code == 200
    return client


@pytest.fixture
def logged_in_page(page: Page, test_user):
    """A browser page that is already logged in as `test_user`, landing on the home page."""
    from pages.login_page import LoginPage
    login_page = LoginPage(page)
    login_page.open().login(test_user["email"], test_user["password"])
    return page
