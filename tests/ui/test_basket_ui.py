
import pytest
from pages.basket_page import BasketPage
from pages.home_page import HomePage
from playwright.sync_api import expect



@pytest.mark.ui
def test_ui18_add_to_basket(page):
    home = HomePage(page).open_home()
    home.add_first_product_to_basket()
    home.basket_btn.click()
    expect(BasketPage(page).rows).to_have_count(1)


@pytest.mark.ui
def test_ui19_remove_from_basket(page):
    home = HomePage(page).open_home()
    home.add_first_product_to_basket()
    home.basket_btn.click()
    basket = BasketPage(page)
    expect(basket.rows).to_have_count(1)
    basket.remove_first()
    expect(basket.rows).to_have_count(0)


@pytest.mark.ui
def test_ui20_updating_quantity_is_reflected_in_basket(page):
    home = HomePage(page).open_home()
    home.add_first_product_to_basket()
    home.basket_btn.click()
    expect(BasketPage(page).rows).to_have_count(1)
    home = HomePage(page).open_home()
    home.add_another_product_to_basket()
    home.basket_btn.click()
    expect(BasketPage(page).rows).to_have_count(2)
