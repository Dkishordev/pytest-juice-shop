from pages.base_page import BasePage


class RegisterPage(BasePage):

    EMAIL_INPUT = "#emailControl"
    PASSWORD_INPUT = "#passwordControl"
    REPEAT_PASSWORD_INPUT = "#repeatPasswordControl"
    SECURITY_ANSWER_INPUT = "#securityAnswerControl"
    REGISTER_BUTTON = "#registerButton"

    def open(self):
        self.goto("/#/register")
        self.dismiss_dialogs()

        self.page.wait_for_selector(
            self.EMAIL_INPUT,
            timeout=10000
        )

        return self

    def register(self, email, password, security_answer="blue"):
        self.page.fill(self.EMAIL_INPUT, email)
        self.page.fill(self.PASSWORD_INPUT, password)
        self.page.fill(self.REPEAT_PASSWORD_INPUT, password)

        self.page.get_by_text("Security Question").click()
        self.page.get_by_role(
            "listbox",
            name="Selection list for the"
        ).click()

        self.page.fill(
            self.SECURITY_ANSWER_INPUT,
            security_answer
        )

        self.page.click(self.REGISTER_BUTTON)
        self.page.wait_for_timeout(500)

        return self
