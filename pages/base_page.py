from __future__ import annotations
from playwright.sync_api import Page
from config.settings import settings


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.base_url = settings.BASE_URL

    def goto(self, path: str = "/"):
        self.page.goto(f"{self.base_url}{path}")
        return self

    def dismiss_dialogs(self):
        for selector in [
            "button[aria-label='Close Welcome Banner']",
            ".cc-dismiss",
            "button:has-text('Me want it!')",
            "button:has-text('Dismiss')",
        ]:
            try:
                locator = self.page.locator(selector)
                if locator.count() > 0 and locator.first.is_visible(timeout=1000):
                    locator.first.click()
            except Exception:
                pass
        return self

    def current_url(self) -> str:
        return self.page.url

    def get_local_storage_token(self) -> str | None:
        return self.page.evaluate("() => window.localStorage.getItem('token')")

    def screenshot(self, name: str):
        self.page.screenshot(path=f"reports/screenshots/{name}.png")
