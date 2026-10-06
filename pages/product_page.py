from playwright.sync_api import Page
from pages.base_page import BasePage


class ProductPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.review_input = page.locator( "#reviewControl, textarea[placeholder='Comment']")
        self.review_submit = page.locator("#submitButton")
        self.add_to_basket_button = page.locator(".btn-basket, button[aria-label='Add to Basket']")

    def open_product_by_index(self, index=0):
        self.page.locator(".mat-grid-tile, app-product").nth(index).click()
        self.page.wait_for_selector("mat-dialog-container", timeout=5000)
        return self

    def submit_review(self, text):
        self.review_input.fill(text)
        self.review_submit.click()
        self.page.wait_for_timeout(500)
        return self

    def add_current_product_to_basket(self):
        self.add_to_basket_button.first.click()
        self.page.wait_for_timeout(500)
        return self


