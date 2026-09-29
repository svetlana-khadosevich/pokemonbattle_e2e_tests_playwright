from playwright.sync_api import Page, Locator, expect


class BasePage:
    BASE_URL = "https://pokemonbattle.ru"

    def __init__(self, page: Page, timeout: int = 5000):
        self.page = page
        self.timeout = timeout

    def open(self, url: str):
        self.page.goto(url)

    def should_be_visible(self, locator: Locator):
        expect(locator).to_be_visible(timeout=self.timeout)

    def should_have_text(self, locator: Locator, text: str):
        expect(locator).to_have_text(text, timeout=self.timeout)

    def should_contain_text(self, locator: Locator, text: str):
        expect(locator).to_contain_text(text, timeout=self.timeout)
