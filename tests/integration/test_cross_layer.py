import re
import uuid
import pytest
from playwright.sync_api import expect
from config import settings
from pages.basket_page import BasketPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from utils.helpers import random_email,random_password


@pytest.mark.integration
def test_int01_api_user_can_login_via_ui(page, test_user):
    LoginPage(page).open().login(test_user["email"], test_user["password"])
    expect(page).not_to_have_url(re.compile(r"#/login"))


@pytest.mark.integration
def test_int02_ui_registered_user_can_login_via_api(page, api_client):
    email = random_email()
    RegisterPage(page).open().register(email, settings.settings.TEST_PASSWORD)
    expect(page).to_have_url(re.compile(r"#/login"))
    r = api_client.login(email, settings.settings.TEST_PASSWORD)
    assert r.status_code == 200 and r.json()["authentication"]["token"]

@pytest.mark.integration
def test_int03_api_basket_item_visible_in_ui(page, authenticated_api_client):
    pid = authenticated_api_client.get_products().json()["data"][0]["id"]
    assert authenticated_api_client.add_to_basket(pid,  quantity=1).status_code == 200
    HomePage(page).open_home().basket_btn.click()
    expect(BasketPage(page).rows).to_have_count(1)


@pytest.mark.integration
def test_int04_feedback_api_to_db(api_client, database):
    comment = f"int-feedback-{uuid.uuid4().hex[:6]}"
    assert api_client.submit_feedback(comment, 4).status_code == 201
    rows = database.query("SELECT rating FROM Feedbacks WHERE comment = ?", (comment,))
    assert rows and rows[0]["rating"] == 4


@pytest.mark.integration
def test_int05_ui_registration_persisted_in_db(page, database):
    email = random_email()
    RegisterPage(page).open().register(email, settings.settings.TEST_PASSWORD)
    expect(page).to_have_url(re.compile(r"#/login"))
    assert len(database.query("SELECT id FROM Users WHERE email = ?", (email,))) == 1
