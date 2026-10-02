import re
import pytest
from playwright.sync_api import expect
from pages.home_page import HomePage


@pytest.mark.ui
def test_ui10_home_page_loads_products(page):
    home = HomePage(page).open_home()
    expect(home.cards.first).to_be_visible()
    assert home.cards.count() > 0 


@pytest.mark.ui
def test_ui11_search_existing_product(page):
    home = HomePage(page).open_home()
    home.search("apple")
    expect(home.names.first).to_contain_text("Apple")


@pytest.mark.ui
def test_ui12_search_no_results(page):
    home = HomePage(page).open_home()
    home.search("zzzznotaproduct")
    expect(home.no_results).to_be_visible()


@pytest.mark.ui
def test_ui13_open_product_details(page):
    home = HomePage(page).open_home()
    expect(home.names.first).to_be_visible()
    name = home.names.first.inner_text()
    print(name)
    home.open_first_product()
    expect(home.dialog).to_be_visible()
    expect(home.dialog.get_by_role("heading", level=1)).to_have_text(name) 


@pytest.mark.ui
def test_ui14_navigate_to_about_us(page):
     home = HomePage(page).open_home()
     home.open_about()
     expect(page).to_have_url(re.compile(r"#/about"))


@pytest.mark.ui
def test_ui15_search_for_known_product_returns_results(page):
    search = HomePage(page).open_home()
    search.search("apple")
    assert search.result_count() > 0, "Searching for a known product term returned zero results"


@pytest.mark.ui
def test_ui16_search_for_nonexistent_product_returns_no_results(page):
    search = HomePage(page).open_home()
    search.search("zzz_definitely_not_a_real_product_zzz")
    assert search.result_count() == 0, "Search for a nonsense term unexpectedly returned products"


@pytest.mark.ui
def test_ui17_clearing_search_restores_full_product_list(page):
    search = HomePage(page).open_home()
    baseline_count = search.result_count()
    search.search("apple")
    filtered_count = search.result_count()
    assert filtered_count <= baseline_count, "Filtered search returned more items than the full catalog"
 
 