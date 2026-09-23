import os

from dotenv import load_dotenv
from playwright.sync_api import expect

from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = f"{BasePage.BASE_URL}/login"

    @property
    def email_input(self):
        return self.page.get_by_role("textbox", name="Почта")

    @property
    def password_input(self):
        return self.page.get_by_role("textbox", name="Пароль")

    @property
    def login_button(self):
        return self.page.get_by_role("button", name="Войти")

    def open_page(self):
        self.page.goto(self.URL)

    def login(self, email=None, password=None):
        if email is None or password is None:
            load_dotenv()
        self.email_input.fill(email or os.getenv("LOGIN"))
        self.password_input.fill(password or os.getenv("PASSWORD"))
        self.login_button.click()
        expect(self.page).to_have_url(f"{BasePage.BASE_URL}/")

    def should_be_login_page(self):
        expect(self.page).to_have_url(self.URL)

