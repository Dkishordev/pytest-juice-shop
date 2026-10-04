import pytest
from utils.helpers import random_email, random_password

@pytest.mark.api
def test_api01_register_returns_201(api_client):
    email = random_email()
    r = api_client.register(email, random_password())
    assert r.status_code == 201
    assert r.json()["data"]["email"] == email



@pytest.mark.api
def test_api02_duplicate_email_rejected(api_client, test_user):
    r = api_client.register(test_user["email"], random_password())
    assert r.status_code == 400


@pytest.mark.api
def test_api03_login_returns_token(api_client, test_user):
    r = api_client.login(test_user["email"], test_user["password"])
    assert r.status_code == 200
    auth = r.json()["authentication"]
    assert auth["token"] and auth["bid"]


@pytest.mark.api
def test_api04_whoami_without_token(api_client):
    r = api_client.whoami()
    assert r.status_code == 200
    assert not r.json().get("user")

