from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.helpers import captcha_bypass


class ContactPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.comment_input = page.locator("#comment")
        self.captchaquestion = page.locator("#captcha")
        self.rating_score= page.get_by_role("slider")
        self.submitbutton = page.locator("#submitButton")
        self.captchafill = page.get_by_role("textbox", name="Field for the result of the")

    def open(self):
        self.goto("/#/contact")
        self.dismiss_dialogs()
        return self

    def submit_feedback(self, database, comment, rating=5):
        self.comment_input.fill(comment)
        self.rating_score.fill(str(rating))
        self.page.wait_for_timeout(500)
        captcha_question = self.captchaquestion.inner_text()
        captchaanswer = captcha_bypass(database,captcha_question)
        self.captchafill.fill(captchaanswer)
        self.submitbutton.click()
        self.page.wait_for_timeout(500)

