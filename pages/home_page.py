from pages.base_page import BasePage



class HomePage(BasePage):


    def __init__(self, page):
        super().__init__(page)
        self.cards = page.locator("mat-card")
        self.names = page.locator("app-product .name")
        self.search_icon = page.locator("#searchQuery")
        self.search_input = page.locator("#searchQuery input")
        self.no_results = page.get_by_text("No results found")
        self.dialog = page.locator("mat-dialog-container")
        self.dialogcontent = page.locator("mat-dialog-content")
        self.account_menu = page.locator("#navbarAccount")
        self.logout_btn = page.locator("#navbarLogoutButton")
        self.login_menu_btn = page.locator("#navbarLoginButton")
        self.basket_btn = page.locator("button[aria-label='Show the shopping cart']")
        self.menu_btn = page.locator("button[aria-label='Open Sidenav']")
        self.product_cards = page.locator(".mat-grid-tile, app-product")

    def open_home(self):
        self.goto("/#/search")
        self.dismiss_dialogs()
        return self

    def search(self, query):
        self.search_icon.click()
        self.search_input.fill(query)
        self.search_input.press("Enter")

    def result_count(self):
        return self.product_cards.count()

    def add_first_product_to_basket(self):
        self.cards.first.locator("button[aria-label='Add to Basket']").click()

    def add_another_product_to_basket(self):
            self.cards.nth(1).locator("button[aria-label='Add to Basket']").click()

    def open_first_product(self):
        self.cards.first.locator("img").click()

    def open_about(self):
        self.menu_btn.click()
        self.page.get_by_text("About Us").first.click()

    def logout(self):
        self.account_menu.click()
        self.logout_btn.click()
