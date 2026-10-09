from pages.base_page import BasePage


class LoginPage(BasePage):


    def __init__(self, page):
        super().__init__(page)
        self.email = page.locator("#email")
        self.password = page.locator("#password")
        self.loginbutton = page.locator("#loginButton")
        self.err_message = page.locator(".error, .mat-mdc-snack-bar-label, mat-error")

    def open(self):
        self.goto("/#/login")
        self.dismiss_dialogs()
        return self

    def login(self, email, password):
        self.email.fill(email)
        self.password.fill(password)
        self.loginbutton.click()
        self.page.wait_for_timeout(500)


    def is_logged_in(self):
        token = self.get_local_storage_token()
        return token is not None
    
    def clear_auth_state(self):
        self.page.evaluate("""
            () => {
                localStorage.clear();
                sessionStorage.clear();
            }
        """)
        self.page.reload()
        self.page.wait_for_load_state("domcontentloaded")

    def get_error_text(self):
        try:
            error = self.err_message.first
            return error.inner_text(timeout=3000)

        except Exception:
            return ""
