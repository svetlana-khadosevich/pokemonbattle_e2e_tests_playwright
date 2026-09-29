import allure

from tests.data.test_data import DAYS, CARD, CARD_NUMBER_INVALID, CARD_DATE_INVALID
from pages.premium_page import PremiumPage


@allure.suite("Скриншот-тесты на форму оплаты")
class TestPremiumDaysScreenshot:
    @allure.title("Пустая форма оплаты")
    def test_screenshot_payment_form_empty(self, authorized_page, assert_snapshot):
        page = authorized_page
        premium_page = PremiumPage(page)
        premium_page.open(premium_page.URL)
        premium_page.should_be_premium_page()
        premium_page.fill_number_of_days(DAYS)
        premium_page.go_to_payment()

        payment_form_screenshot = premium_page.payment_form.screenshot()
        assert_snapshot(payment_form_screenshot, "empty_payment_form.png")

    @allure.title("Заполненная форма оплаты")
    def test_screenshot_payment_form_positive(self, authorized_page, assert_snapshot):
        page = authorized_page
        premium_page = PremiumPage(page)
        premium_page.open(premium_page.URL)
        premium_page.should_be_premium_page()
        premium_page.fill_number_of_days(DAYS)
        premium_page.go_to_payment()
        premium_page.buying_premium_card_data(CARD)

        payment_form_screenshot = premium_page.payment_form.screenshot()
        assert_snapshot(payment_form_screenshot, "filled_payment_form.png")

    @allure.title("Неверный номер карты")
    def test_screenshot_payment_form_wrong_card_number(self, authorized_page, assert_snapshot):
        page = authorized_page
        premium_page = PremiumPage(page)
        premium_page.open(premium_page.URL)
        premium_page.should_be_premium_page()
        premium_page.fill_number_of_days(DAYS)
        premium_page.go_to_payment()
        premium_page.buying_premium_card_data(CARD_NUMBER_INVALID)
        premium_page.should_be_error_message_card_number()

        payment_form_screenshot = premium_page.payment_form.screenshot()
        assert_snapshot(payment_form_screenshot, "payment_form_wrong_card_number.png")

    @allure.title("Неверная дата")
    def test_screenshot_payment_form_wrong_card_date(self, authorized_page, assert_snapshot):
        page = authorized_page
        premium_page = PremiumPage(page)
        premium_page.open(premium_page.URL)
        premium_page.should_be_premium_page()
        premium_page.fill_number_of_days(DAYS)
        premium_page.go_to_payment()
        premium_page.buying_premium_card_data(CARD_DATE_INVALID)
        premium_page.should_be_error_message_card_date()

        payment_form_screenshot = premium_page.payment_form.screenshot()
        assert_snapshot(payment_form_screenshot, "payment_form_wrong_card_date.png")