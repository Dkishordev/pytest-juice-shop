import pytest


@pytest.mark.api
def test_api11_get_all_products_returns_a_nonempty_list(api_client):
    resp = api_client.get_products()
    assert resp.status_code == 200
    products = resp.json().get("data", [])
    assert len(products) > 0


@pytest.mark.api
def test_api12_get_all_products_items_have_required_fields(api_client):
    resp = api_client.get_products()
    products = resp.json().get("data", [])
    assert products, "No products returned to validate field shape"
    first = products[0]
    for field in ("id", "name", "price", "description"):
        assert field in first


@pytest.mark.api
def test_api13_get_single_product_by_id_returns_matching_id(api_client):
    all_products = api_client.get_products().json().get("data", [])
    assert all_products
    target_id = all_products[0]["id"]
    resp = api_client.get_product(target_id)
    print(resp)
    assert resp.status_code == 200
    assert resp.json().get("data", {}).get("id") == target_id

@pytest.mark.api
def test_api14_get_nonexistent_product_returns_404(api_client):
    resp = api_client.get_product(999999)
    assert resp.status_code == 404

@pytest.mark.api
def test_api15_search_products_returns_only_matching_items(api_client):
    resp = api_client.search_products("apple")
    assert resp.status_code == 200
    results = resp.json().get("data", [])
    assert all("apple" in (p.get("name", "") + p.get("description", "")).lower() for p in results)

@pytest.mark.api
@pytest.mark.smoke
def test_api16_get_products(api_client):
    r = api_client.get_products()
    assert r.status_code == 200
    assert len(r.json()["data"]) > 0


@pytest.mark.api
def test_api17_search_matching_term(api_client):
    r = api_client.search_products("apple")
    assert r.status_code == 200
    data = r.json()["data"]
    assert len(data) > 0
    assert any("apple" in p["name"].lower() for p in data)


@pytest.mark.api
def test_api18_search_non_matching_term(api_client):
    r = api_client.search_products("zzzznotaproduct")
    assert r.status_code == 200
    assert r.json()["data"] == []


@pytest.mark.api
def test_api19_get_product_by_id(api_client):
    pid = api_client.get_products().json()["data"][0]["id"]
    r = api_client.get_product(pid)
    assert r.status_code == 200
    assert r.json()["data"]["id"] == pid

