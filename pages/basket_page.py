from pages.base_page import BasePage


class BasketPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.checkout = page.locator("#checkoutButton")
        self.item_rows = page.locator("mat-row, tr")
        self.rows = page.locator("app-purchase-basket mat-row")
    



    def open(self):
        self.goto("/#/basket")
        self.dismiss_dialogs()
        return self


    def remove_first(self):
        self.rows.first.locator("button:has(.fa-trash-alt)").click()
