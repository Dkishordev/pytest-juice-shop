from playwright.sync_api import Page
from pages.base_page import BasePage


class SearchPage(BasePage):

    PRODUCT_CARDS = ".mat-grid-tile, app-product"

    def open_home(self):
        self.goto("/#/search")
        self.dismiss_dialogs()
        return self

    def search(self, query):
        self.page.get_by_role("button", name="Open search").click()
        self.page.get_by_role("textbox").fill(query)
        self.page.get_by_role("textbox").press("Enter") 
        self.page.wait_for_timeout(800)
        return self

    def result_count(self):
        return self.page.locator(self.PRODUCT_CARDS).count()

    def page_contains_unescaped_script_execution(self):
        # Check whether the XSS test payload was actually executed.
        return self.page.evaluate(
            "() => window.__xss_fired === true"
        )