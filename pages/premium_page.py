import allure

from playwright.sync_api import expect

from pages.base_page import BasePage


class PremiumPage(BasePage):
    URL = f"{BasePage.BASE_URL}/premium"

    @property
    def card_number_input(self):
        return self.page.get_by_role("textbox", name="0000 0000 0000")

    @property
    def date_input(self):
        return self.page.get_by_role("textbox", name="/00")

    @property
    def cvv_input(self):
        return self.page.get_by_role("textbox", name="000", exact=True)

    @property
    def name_input(self):
        return self.page.get_by_role("textbox", name="GERMAN DOLNIKOV")

    @property
    def ds_code_input(self):
        return self.page.get_by_role("textbox", name="00000")

    @property
    def pay_button(self):
        return self.page.get_by_role("button", name="Оплатить")

    @property
    def payment_button(self):
        return self.page.get_by_role("button", name="Перейти к оплате")

    @property
    def cancel_payment_button(self):
        return self.page.get_by_role("button", name="Отменить подписку")

    @property
    def days_input(self):
        return self.page.get_by_placeholder(" ")

    def fill_number_of_days(self, days: str):
        self.days_input.fill(days)

    @allure.step("Покупка Премиума")
    def buying_premium(self, card: dict):
        self.card_number_input.press_sequentially(card["number"], delay=50)
        self.date_input.press_sequentially(card["date"], delay=50)
        self.cvv_input.press_sequentially(card["cvv"], delay=50)
        self.name_input.press_sequentially(card["name"], delay=50)
        self.pay_button.click()
        expect(self.page).to_have_url(f"{BasePage.BASE_URL}/payment_3ds")
        self.ds_code_input.fill(card["3ds_code"])
        expect(self.pay_button).to_be_enabled(timeout=15000)
        self.pay_button.click()
        expect(self.page).to_have_url(f"{BasePage.BASE_URL}/payment_success")

    @allure.step("Переход на страницу покупки Премиума")
    def go_to_payment(self):
        self.should_be_visible(self.payment_button)
        self.payment_button.click()
        expect(self.page).to_have_url(f"{BasePage.BASE_URL}/payment/0")

    def should_be_premium_page(self):
        expect(self.page).to_have_url(self.URL)

    def should_be_successfull(self):
        self.should_be_visible(self.page.get_by_role("heading", name="Покупка прошла успешно"))

    @allure.step("Отмена Премиума")
    def cancel_premium(self):
        expect(self.cancel_payment_button).to_be_enabled(timeout=15000)
        self.cancel_payment_button.click()
        expect(self.page.get_by_text("Вы уверены, что хотите отменить подписку?")).to_be_visible()
        expect(self.cancel_payment_button).to_be_enabled(timeout=15000)
        self.cancel_payment_button.click()
        self.should_contain_text(self.page.locator("body"), "Вы отменили подписку")
