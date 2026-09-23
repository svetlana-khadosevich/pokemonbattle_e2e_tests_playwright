import os

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

    def fill_number_of_days(self):
        self.page.get_by_placeholder(" ").fill(os.getenv('DAYS'))

    @property
    def cancel_payment_button(self):
        return self.page.get_by_role("button", name = "Отменить подписку")

    def open_page(self):
        self.page.goto(self.URL)

    def buying_premium(self):
        self.card_number_input.press_sequentially((os.getenv('CARD_NUMBER')), delay=50)
        self.date_input.press_sequentially((os.getenv("CARD_DATE")), delay=50)
        self.cvv_input.press_sequentially((os.getenv("CARD_CVV")), delay=50)
        self.name_input.press_sequentially((os.getenv("CARD_NAME")), delay=50)
        self.pay_button.click()
        expect(self.page).to_have_url(f"{BasePage.BASE_URL}/payment_3ds")
        self.ds_code_input.fill(os.getenv("CARD_3DS_CODE"))
        expect(self.page.get_by_role("button", name="Оплатить")).to_be_enabled(timeout=15000)
        self.pay_button.click()
        expect(self.page).to_have_url(f"{BasePage.BASE_URL}/payment_success")

    def go_to_payment(self):
        expect(self.payment_button).to_be_enabled(timeout=5000)
        self.payment_button.click()
        expect(self.page).to_have_url(f"{BasePage.BASE_URL}/payment/0")

    def should_be_premium_page(self):
        expect(self.page).to_have_url(self.URL)

    def should_be_successfull(self):
        expect(self.page.get_by_role("heading", name="Покупка прошла успешно")).to_be_visible()

    def cancel_premium(self):
        expect(self.page.get_by_role("button", name="Отменить подписку")).to_be_enabled(timeout=15000)
        self.cancel_payment_button.click()
        self.should_be_premium_page()
        expect(self.page.get_by_text("Вы уверены, что хотите отменить подписку?")).to_be_visible()
        expect(self.page.get_by_role("button", name="Отменить подписку")).to_be_enabled(timeout=15000)
        self.cancel_payment_button.click()
        expect(self.page.get_by_text("Вы отменили подписку :(")).to_be_visible()







