from __future__ import annotations
from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    EMAIL_INPUT = "#email"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#loginButton"
    ERROR_MESSAGE = ".error, .mat-mdc-snack-bar-label, mat-error"

    def __init__(self, page: Page):
        super().__init__(page)

    def open(self) -> "LoginPage":
        self.goto("/#/login")
        self.dismiss_dialogs()
        self.page.wait_for_selector(self.EMAIL_INPUT, timeout=10000)
        return self

    def login(self, email: str, password: str) -> "LoginPage":
        self.page.fill(self.EMAIL_INPUT, email)
        self.page.fill(self.PASSWORD_INPUT, password)
        self.page.click(self.LOGIN_BUTTON)
        self.page.wait_for_timeout(500)
        return self

    def is_logged_in(self) -> bool:
        return self.get_local_storage_token() is not None

    def get_error_text(self) -> str:
        try:
            return self.page.locator(self.ERROR_MESSAGE).first.inner_text(timeout=3000)
        except Exception:
            return ""
