
import pytest
import re
from pages.contact_page import ContactPage
from pages.home_page import HomePage
from pages.product_page import ProductPage




@pytest.mark.integration
def test_int06_feedback_submitted_via_ui_is_persisted_in_database(page, database):
    marker = "INTEGRATIONTEST_FEEDBACK_MARKER"
    ContactPage(page).open().submit_feedback(database,f"Great store! {marker}", rating=4)
    page.wait_for_timeout(500)
    count = database.count_feedback_containing(marker)
    assert count >= 1, "Feedback submitted through the UI was not found in the Feedbacks table"

@pytest.mark.integration
def test_int07_review_submitted_via_api_is_visible_on_product_page(logged_in_page, authenticated_api_client):

    marker = "INTEGRATIONTEST_REVIEW_MARKER"
    resp = authenticated_api_client.submit_review(1, f"Solid product. {marker}")
    assert resp.status_code in (200, 201), "Could not submit a review via the API to set up this test"
    HomePage(logged_in_page).open_home()
    logged_in_page.wait_for_timeout(5000)
    ProductPage(logged_in_page).open_product_by_index(0)
    logged_in_page.wait_for_timeout(5000)
    logged_in_page.get_by_role("button", name=re.compile(r"^Reviews")).click()
    page_text = logged_in_page.inner_text("mat-dialog-container")
    print(page_text)
    assert marker in page_text, "Review submitted via the API is not visible on the product detail page"
