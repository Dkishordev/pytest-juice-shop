from pages.base_page import BasePage


class RegisterPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.email = page.locator("#emailControl")
        self.password = page.locator("#passwordControl")
        self.repeat = page.locator("#repeatPasswordControl")
        self.question = page.get_by_text("Security Question")
        self.answer = page.locator("#securityAnswerControl")
        self.submit = page.locator("#registerButton")
        self.errors = page.locator("mat-error")

    def open(self):
        self.goto("/#/register")
        self.dismiss_dialogs()
        return self

    def register(self, email, password, repeat=None, answer="blue"):
        self.email.fill(email)
        self.password.fill(password)
        self.repeat.fill(repeat or password)
        self.question.click()
        self.page.get_by_role(
            "listbox",
            name="Selection list for the"
        ).click()
        self.answer.fill(answer)
        self.submit.click()
        self.page.wait_for_timeout(500)

