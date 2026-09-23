import os
import requests

from playwright.sync_api import expect

from pages.premium_page import PremiumPage
from pages.main_page import MainPage
from pages.trainer_page import TrainerPage


# 1. переход на страницу тренера с главной
def test_go_to_trainer_page(authorized_page):
    page = authorized_page
    main_page=MainPage(page)
    trainer_page = TrainerPage(page)
    expect(main_page.trainer_badge).to_be_visible()
    main_page.trainer_badge.click()
    trainer_page.should_be_trainer_page()


# 2. переход со страницы тренера в раздел покупки Премиума
def test_go_to_premium_page(authorized_page):
    page = authorized_page
    main_page = MainPage(page)
    trainer_page = TrainerPage(page)
    premium_page = PremiumPage(page)
    trainer_page.open_page()
    expect(main_page.trainer_badge).to_be_visible()
    # переход на страницу тренера
    main_page.trainer_badge.click()
    trainer_page.should_be_trainer_page()
    # переход со страницы тренера в раздел покупки Премиума
    trainer_page.should_find_pokemon_premium()
    trainer_page.locator_qa_premium()
    premium_page.should_be_premium_page()


# 3. проверка активности ачивки «Начало большого пути»
def test_check_achievement(authorized_page):
    page = authorized_page
    main_page = MainPage(page)
    trainer_page = TrainerPage(page)
    trainer_page.open_page()
    expect(main_page.trainer_badge).to_be_visible()
    main_page.trainer_badge.click()
    trainer_page.should_be_trainer_page()
    trainer_page.achievement_active()


# 4. Покупка Премиум
def test_buy_premium(authorized_page, premium_disabled):
    page = authorized_page
    premium_page = PremiumPage(page)
    premium_page.open_page()
    premium_page.should_be_premium_page()
    premium_page.fill_number_of_days()
    premium_page.go_to_payment()
    premium_page.buying_premium()
    premium_page.should_be_successfull()
    me = requests.get(os.getenv("POKEMON_URL") + "/v2/me",
                      headers={"trainer_token": os.getenv("POKEMONBATTLE_TOKEN")})
    body = me.json()
    assert body["data"][0]["is_premium"] is True


# 5. Отмена Премиум
def test_cancel_premium(authorized_page, premium_enabled):
    page = authorized_page
    premium_page = PremiumPage(page)
    premium_page.open_page()
    premium_page.should_be_premium_page()
    premium_page.cancel_premium()
    me = requests.get(os.getenv("POKEMON_URL") + "/v2/me",
                      headers={"trainer_token": os.getenv("POKEMONBATTLE_TOKEN")})
    body = me.json()
    assert body["data"][0]["is_premium"] is False
