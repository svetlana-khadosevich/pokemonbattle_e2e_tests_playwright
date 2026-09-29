import allure

from pages.premium_page import PremiumPage


@allure.suite("Скриншот-тесты на блок ввода количества дней при покупке Премиума")
class TestPremiumDaysScreenshot:
    @allure.title("До 30 дней")
    def test_screenshot_premium_up_to_30_days(self, authorized_page, assert_snapshot):
        page = authorized_page
        premium_page = PremiumPage(page)
        premium_page.open(premium_page.URL)
        premium_page.should_be_premium_page()
        premium_page.fill_number_of_days("20")
        premium_page.should_be_premium_cost_visible()

        premium_days_block_screenshot = premium_page.premium_days_block.screenshot()
        assert_snapshot(premium_days_block_screenshot, "premium_days_block_up_to_30.png")

    @allure.title("30–180 дней")
    def test_screenshot_premium_30_to_180_days(self, authorized_page, assert_snapshot):
        page = authorized_page
        premium_page = PremiumPage(page)
        premium_page.open(premium_page.URL)
        premium_page.should_be_premium_page()
        premium_page.fill_number_of_days("180")
        premium_page.should_be_premium_cost_visible()

        premium_days_block_screenshot = premium_page.premium_days_block.screenshot()
        assert_snapshot(premium_days_block_screenshot, "premium_days_block_30_to_180.png")

    @allure.title("180–365 дней")
    def test_screenshot_premium_180_to_365_days(self, authorized_page, assert_snapshot):
        page = authorized_page
        premium_page = PremiumPage(page)
        premium_page.open(premium_page.URL)
        premium_page.should_be_premium_page()
        premium_page.fill_number_of_days("250")
        premium_page.should_be_premium_cost_visible()

        premium_days_block_screenshot = premium_page.premium_days_block.screenshot()
        assert_snapshot(premium_days_block_screenshot, "premium_days_block_180_to_365.png")

    @allure.title("Более 365 дней")
    def test_screenshot_premium_more_than_365_days(self, authorized_page, assert_snapshot):
        page = authorized_page
        premium_page = PremiumPage(page)
        premium_page.open(premium_page.URL)
        premium_page.should_be_premium_page()
        premium_page.fill_number_of_days("400")
        premium_page.should_be_premium_cost_visible()

        premium_days_block_screenshot = premium_page.premium_days_block.screenshot()
        assert_snapshot(premium_days_block_screenshot, "premium_days_block_more_than_365.png")
