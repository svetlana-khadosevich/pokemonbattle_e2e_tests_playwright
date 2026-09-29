import os
import requests
import allure


from pages.premium_page import PremiumPage
from pages.main_page import MainPage
from pages.trainer_page import TrainerPage
from tests.data.test_data import DAYS, CARD


@allure.suite("Тесты со страницы тренера")
class TestTrainerPage:
    @allure.title("Переход на страницу тренера с главной")
    def test_go_to_trainer_page(self, authorized_page):
        page = authorized_page
        main_page = MainPage(page)
        trainer_page = TrainerPage(page)
        main_page.go_to_trainer_page()
        trainer_page.should_be_trainer_page()


    @allure.title("Переход со страницы тренера в раздел покупки Премиума")
    def test_go_to_premium_page(self, authorized_page):
        page = authorized_page
        main_page = MainPage(page)
        trainer_page = TrainerPage(page)
        premium_page = PremiumPage(page)
        trainer_page.open(trainer_page.URL)
        # переход на страницу тренера
        main_page.go_to_trainer_page()
        trainer_page.should_be_trainer_page()
        # переход со страницы тренера в раздел покупки Премиума
        trainer_page.should_find_pokemon_premium()
        trainer_page.go_to_premium()
        premium_page.should_be_premium_page()


    @allure.title("Проверка активности ачивки «Начало большого пути»")
    def test_check_achievement(self, authorized_page):
        page = authorized_page
        main_page = MainPage(page)
        trainer_page = TrainerPage(page)
        trainer_page.open(trainer_page.URL)
        main_page.go_to_trainer_page()
        trainer_page.should_be_trainer_page()
        trainer_page.achievement_active()


@allure.suite("Тесты на покупку и отмену Премиум")
class TestPremium:
    @allure.title("Покупка Премиум")
    def test_buy_premium(self, authorized_page, premium_disabled):
        page = authorized_page
        premium_page = PremiumPage(page)
        premium_page.open(premium_page.URL)
        premium_page.should_be_premium_page()
        premium_page.fill_number_of_days(DAYS)
        premium_page.go_to_payment()
        premium_page.buying_premium(CARD)
        premium_page.should_be_successfull()
        with allure.step("Проверка отмены премиума через API-запрос /me"):
            me = requests.get(os.getenv("POKEMON_URL") + "/v2/me",
                              headers={"trainer_token": os.getenv("POKEMONBATTLE_TOKEN")})
            body = me.json()
            assert body["data"][0]["is_premium"] is True


    @allure.title("Отмена Премиум")
    def test_cancel_premium(self, authorized_page, premium_enabled):
        page = authorized_page
        premium_page = PremiumPage(page)
        premium_page.open(premium_page.URL)
        premium_page.should_be_premium_page()
        premium_page.cancel_premium()
        with allure.step("Проверка отмены премиума через API-запрос /me"):
            me = requests.get(os.getenv("POKEMON_URL") + "/v2/me",
                              headers={"trainer_token": os.getenv("POKEMONBATTLE_TOKEN")})
            body = me.json()
            assert body["data"][0]["is_premium"] is False
