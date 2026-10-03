
import pytest


@pytest.mark.db
def test_newly_registered_user_exists_in_users_table(database, test_user):
    row = database.get_user_by_email(test_user["email"])
    assert row is not None, "Registered user was not found in the Users table"
    assert row["email"] == test_user["email"]


@pytest.mark.db
def test_user_password_is_not_stored_in_plaintext(database, test_user):
    row = database.get_user_by_email(test_user["email"])
    assert row is not None, "Test user not found in DB"
    stored_password = row["password"]
    assert stored_password != test_user["password"], "Password is stored in plaintext in the database!"
    assert len(stored_password) >= 32, "Stored password value looks too short to be a proper hash"


@pytest.mark.db
def test_users_table_enforces_unique_email(database, test_user):
    matches = database.query("SELECT COUNT(*) as c FROM Users WHERE email = ?", (test_user["email"],))
    assert matches[0]["c"] == 1, f"Expected exactly one row for {test_user['email']}, found {matches[0]['c']}"
