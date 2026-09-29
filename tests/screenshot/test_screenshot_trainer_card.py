import allure

from pages.main_page import MainPage
from pages.trainer_page import TrainerPage

@allure.suite("Скриншот-тест на карточку характеристик тренера")
class TestPremiumDaysScreenshot:
    @allure.title("Карточка тренера")
    def test_screenshot_trainer_card(self, authorized_page, assert_snapshot):
        page = authorized_page
        main_page = MainPage(page)
        trainer_page = TrainerPage(page)
        main_page.go_to_trainer_page()
        trainer_page.should_be_trainer_page()

        trainer_card_screenshot = trainer_page.trainer_stats.screenshot(mask=[trainer_page.beginning_achievement,
                                                                             trainer_page.achievements,
                                                                             trainer_page.sliders,
                                                                             trainer_page.pokemon_stats,
                                                                             trainer_page.level_stats
                                                                             ])
        assert_snapshot(trainer_card_screenshot, "trainer_card2.png")
