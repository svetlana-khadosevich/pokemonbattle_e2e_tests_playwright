import os
import re

from dotenv import load_dotenv
from playwright.sync_api import expect

from pages.base_page import BasePage


class TrainerPage(BasePage):
    load_dotenv()
    URL = f"{BasePage.BASE_URL}/trainer/{os.getenv('TRAINER_ID')}"

    @property
    def trainer_stats(self):
        return self.page.locator(".single_page_body_content_inner_box")

    @property
    def beginning_achievement(self):
        return self.page.locator("#beginning")

    @property
    def achievements(self):
        return self.page.locator(".achievements")

    @property
    def sliders(self):
        return self.page.locator(".single_page_body_content_inner_top_list_attr_one_slide")

    @property
    def pokemon_stats(self):
        return self.page.locator('//span[text()="Покеболы"]/following-sibling::*')

    @property
    def level_stats(self):
        return self.page.locator('//span[text()="Уровень"]/following-sibling::*')

    def open_page(self):
        self.open(self.URL)

    def should_be_trainer_page(self):
        expect(self.page).to_have_url(self.URL)
        self.should_be_visible(self.achievements)

    def achievement_active(self):
        expect(self.page.locator("#beginning")).to_have_class(re.compile(r"\bactive\b"))

    def should_find_pokemon_premium(self):
        self.should_be_visible(self.page.get_by_text("Pokemon Premium", exact=False))

    def go_to_premium(self):
        self.page.locator('[data-qa="premium"]').click()
