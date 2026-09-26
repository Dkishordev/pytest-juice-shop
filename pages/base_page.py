from playwright.sync_api import Page
from config.settings import settings


class BasePage:

    def __init__(self, page):
        self.page = page
        self.base_url = settings.BASE_URL

    def goto(self, path="/"):
        self.page.goto(self.base_url + path)
        return self

    def dismiss_dialogs(self):
        buttons = [
            "button[aria-label='Close Welcome Banner']",
            ".cc-dismiss",
            "button:has-text('Me want it!')",
            "button:has-text('Dismiss')"
        ]

        for button in buttons:
            try:
                element = self.page.locator(button)

                if element.count() > 0:
                    if element.first.is_visible(timeout=1000):
                        element.first.click()

            except Exception:
                pass

        return self

    def current_url(self):
        return self.page.url

    def get_local_storage_token(self):
        return self.page.evaluate(
            "() => window.localStorage.getItem('token')"
        )

    def screenshot(self, name):
        self.page.screenshot(
            path=f"reports/screenshots/{name}.png"
        )
