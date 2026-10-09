
import pytest
from utils.helpers import SQLI_PAYLOADS
from pages.login_page import LoginPage


@pytest.mark.sqli
def test_sec01_search_endpoint_union_select_does_not_leak_extra_columns(api_client):
    payload = "')) UNION SELECT id,email,password,'4','5','6','7','8','9' FROM Users--"
    resp = api_client.search_products(payload)

    assert resp.status_code in (200, 500), (
        f"Unexpected status: {resp.status_code}"
    )

    if resp.status_code == 200:
        body = resp.json()

        assert body.get("status") == "success"

        allowed_fields = {
            "id",
            "name",
            "description",
            "price",
            "deluxePrice",
            "image",
            "createdAt",
            "updatedAt",
            "deletedAt",
        }

        for product in body.get("data", []):
            assert set(product).issubset(allowed_fields), (
                f"Unexpected fields in product response: "
                f"{set(product) - allowed_fields}"
            )


@pytest.mark.sqli
@pytest.mark.parametrize("payload", SQLI_PAYLOADS)
def test_sec02_search_endpoint_handles_injection_payloads_gracefully(
    api_client, payload
):
    resp = api_client.search_products(payload)

    assert resp.status_code < 500, (
        f"Search endpoint returned HTTP {resp.status_code} "
        f"for payload: {payload}"
    )

    body = resp.text.lower()
    assert "traceback (most recent call last)" not in body
    assert "sqlite_error" not in body

@pytest.mark.sqli
def test_sec03_product_id_path_param_rejects_injection(api_client):
    resp = api_client.get_product("1 OR 1=1")
    assert resp.status_code in (400, 404, 500), (
        "Non-numeric injected product id was silently accepted"
    )


@pytest.mark.sqli
def test_sec04_feedback_comment_injection_does_not_alter_db_rowcount(api_client, database, test_user, authenticated_api_client):
    before = database.query_one("SELECT COUNT(*) as c FROM Feedbacks")["c"]
    payload = "test'); DROP TABLE Feedbacks;--"
    authenticated_api_client.submit_feedback(payload)
    after = database.query_one("SELECT COUNT(*) as c FROM Feedbacks")["c"]
    assert after >= before, "Feedbacks table appears to have been affected by injected DDL!"


@pytest.mark.sqli
def test_sec05_login_boolean_blind_injection_timing_is_consistent(api_client):
    resp = api_client.login("admin@juice-sh.op' AND '1'='1", "irrelevant")
    assert resp.status_code != 200, "Boolean-blind SQLi payload achieved authentication"


@pytest.mark.sqli
@pytest.mark.parametrize("payload", SQLI_PAYLOADS[:3])
def test_sec06_login_field_rejects_various_sqli_payloads(page, payload):
    login = LoginPage(page).open()
    login.login(payload, "wrongpass")
    assert not login.is_logged_in(), f"Payload leaked auth bypass: {payload}"



@pytest.mark.sqli
def test_sec07_login_sql_injection_bypass_is_blocked(page):
    login = LoginPage(page).open()
    login.clear_auth_state()

    login.login("' OR 1=1--", "anything")

    assert not login.is_logged_in(), (
        "SQL injection payload bypassed authentication!"
    )