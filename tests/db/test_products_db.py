
import pytest


@pytest.mark.db
def test_products_table_exists_and_has_rows(database):
    tables = database.list_tables()
    assert "Products" in tables, "Products table is missing from the database"
    rows = database.query("SELECT COUNT(*) as c FROM Products")
    assert rows[0]["c"] > 0, "Products table has no seeded rows"


@pytest.mark.db
def test_every_product_has_a_nonnegative_price(database):
    rows = database.query("SELECT id, price FROM Products")
    bad = [r for r in rows if r["price"] is None or r["price"] < 0]
    assert not bad, f"Products with invalid/negative price found: {bad}"


@pytest.mark.db
def test_every_product_has_a_nonempty_name(database):
    rows = database.query("SELECT id, name FROM Products")
    bad = [r for r in rows if not r["name"] or not r["name"].strip()]
    assert not bad, f"Products with empty name found: {bad}"

@pytest.mark.smoke
@pytest.mark.db
def test_product_count_via_db_matches_product_count_via_api(database, api_client):
    db_count = database.query_one("SELECT COUNT(*) as c FROM Products where deletedAt is NULL")["c"]
    api_products = api_client.get_products().json().get("data", [])
    assert db_count == len(api_products), (
        f"Product count mismatch: DB has {db_count}, API returned {len(api_products)}"
    )
