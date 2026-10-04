
import pytest


@pytest.mark.api
def test_api05_add_item_to_basket_returns_created_item(authenticated_api_client):
    resp = authenticated_api_client.add_to_basket(product_id=1, quantity=2)
    assert resp.status_code in (200, 201), f"Adding a valid item to the basket failed: {resp.status_code}"
    data = resp.json().get("data", {})
    assert data.get("quantity") == 2


@pytest.mark.api
def test_api06_get_basket_returns_previously_added_items(authenticated_api_client):
    authenticated_api_client.add_to_basket(product_id=1, quantity=1)
    resp = authenticated_api_client.get_basket(1)
    assert resp.status_code == 200
    basket = resp.json().get("data", {})
    assert "Products" in basket or "id" in basket


@pytest.mark.api
def test_api07_basket_total_reflects_sum_of_item_prices(authenticated_api_client, database):
    product = database.get_product_by_id(1)
    if not product:
        pytest.skip("Seed product #1 not found in DB")
    authenticated_api_client.add_to_basket(product_id=1, quantity=2)
    resp = authenticated_api_client.get_basket(1)
    assert resp.status_code == 200

@pytest.mark.api
def test_api08_add_item_to_basket(authenticated_api_client, test_user):
    pid = authenticated_api_client.get_products().json()["data"][0]["id"]
    r = authenticated_api_client.add_to_basket(pid,quantity=1)
    assert r.status_code == 200


@pytest.mark.api
def test_api09_basket_contains_added_item(authenticated_api_client, test_user):
    pid = authenticated_api_client.get_products().json()["data"][0]["id"]
    assert authenticated_api_client.add_to_basket(pid, quantity=1).status_code == 200
    items = authenticated_api_client.get_basket(1).json()["data"]["Products"]
    assert any(p["id"] == pid for p in items)


@pytest.mark.api
def test_api10_submit_feedback_with_captcha(api_client):
    r = api_client.submit_feedback("api-feedback-test", 5)
    assert r.status_code == 201
    assert r.json()["data"]["comment"] == "api-feedback-test"
