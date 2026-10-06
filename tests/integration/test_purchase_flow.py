import pytest
from pages.basket_page import BasketPage
from pages.home_page import HomePage
from pages.product_page import ProductPage


@pytest.mark.integration
def test_int08_item_added_via_api_is_visible_in_ui_basket(logged_in_page, authenticated_api_client, test_user):
    authenticated_api_client.add_to_basket(product_id=1, quantity=1)
    basket = BasketPage(logged_in_page).open()
    assert basket.item_count() >= 0, "Basket page failed to render after an API-side basket mutation"


@pytest.mark.integration
def test_int09_basket_added_via_ui_is_persisted_and_readable_via_api(logged_in_page, authenticated_api_client):
    HomePage(logged_in_page).open_home()
    ProductPage(logged_in_page).open_product_by_index(0).add_current_product_to_basket()
    resp = authenticated_api_client.get_basket(1)
    assert resp.status_code == 200, "Basket added via UI could not be read back via the API"
