
import pytest
import uuid


@pytest.mark.db
def test_db05_products_table_exists_and_has_rows(database):
    tables = database.list_tables()
    assert "Products" in tables, "Products table is missing from the database"
    rows = database.query("SELECT COUNT(*) as c FROM Products")
    assert rows[0]["c"] > 0, "Products table has no seeded rows"


@pytest.mark.db
def test_db06_every_product_has_a_nonnegative_price(database):
    rows = database.query("SELECT id, price FROM Products")
    bad = [r for r in rows if r["price"] is None or r["price"] < 0]
    assert not bad, f"Products with invalid/negative price found: {bad}"


@pytest.mark.db
def test_db07_every_product_has_a_nonempty_name(database):
    rows = database.query("SELECT id, name FROM Products")
    bad = [r for r in rows if not r["name"] or not r["name"].strip()]
    assert not bad, f"Products with empty name found: {bad}"


@pytest.mark.db
def test_db08_product_count_via_db_matches_product_count_via_api(database, api_client):
    db_count = database.query_one("SELECT COUNT(*) as c FROM Products where deletedAt is NULL")["c"]
    api_products = api_client.get_products().json().get("data", [])
    assert db_count == len(api_products), (
        f"Product count mismatch: DB has {db_count}, API returned {len(api_products)}"
    )

@pytest.mark.db
def test_db09_basket_item_persisted(authenticated_api_client, test_user, database):
    pid = authenticated_api_client.get_products().json()["data"][0]["id"]

    basket = database.query(
        "SELECT id FROM Baskets WHERE UserId = ?",
        (test_user["id"],)
    )
    assert basket, f"No basket found for user {test_user['id']}"
    basket_id = basket[0]["id"]

    response = authenticated_api_client.add_to_basket(
        pid,
        quantity=2,
        basket_id=basket_id
    )
    assert response.status_code == 200, response.text
    rows = database.query(
        "SELECT quantity FROM BasketItems "
        "WHERE BasketId = ? AND ProductId = ?",
        (basket_id, pid)
    )
    assert rows and rows[0]["quantity"] == 2


@pytest.mark.db
def test_db10_feedback_persisted(api_client, database):
    comment = f"db-feedback-{uuid.uuid4().hex[:6]}"
    response = api_client.submit_feedback(comment, 3)
    assert response.status_code == 201, response.text
    rows = database.query("SELECT rating FROM Feedbacks WHERE comment = ?", (comment,))
    assert rows and rows[0]["rating"] == 3