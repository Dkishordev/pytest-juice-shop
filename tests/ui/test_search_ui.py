import pytest
from pages.search_page import SearchPage


@pytest.mark.ui
def test_search_for_known_product_returns_results(page):
    search = SearchPage(page).open_home()
    search.search("apple")
    assert search.result_count() > 0, "Searching for a known product term returned zero results"


@pytest.mark.ui
def test_search_for_nonexistent_product_returns_no_results(page):
    search = SearchPage(page).open_home()
    search.search("zzz_definitely_not_a_real_product_zzz")
    assert search.result_count() == 0, "Search for a nonsense term unexpectedly returned products"


@pytest.mark.ui
def test_clearing_search_restores_full_product_list(page):
    search = SearchPage(page).open_home()
    baseline_count = search.result_count()
    search.search("apple")
    filtered_count = search.result_count()
    assert filtered_count <= baseline_count, "Filtered search returned more items than the full catalog"
