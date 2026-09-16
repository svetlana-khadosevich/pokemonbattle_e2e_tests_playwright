import os
import re

import requests

from playwright.sync_api import expect

from tests.data.test_data import TEST_CARD


# 1. переход на страницу тренера с главной
def test_go_to_trainer_page(authorized_page):
    page = authorized_page
    expect(page.get_by_role("link", name=f"ID {os.getenv('TRAINER_ID')} логотип")).to_be_visible()
    page.get_by_role("link", name=f"ID {os.getenv('TRAINER_ID')} логотип").click()
    page.wait_for_url(f"https://pokemonbattle.ru/trainer/{os.getenv('TRAINER_ID')}")


# 2. переход со страницы тренера в раздел покупки Премиума
def test_go_to_premium_page(authorized_page):
    page = authorized_page
    page.goto(f"https://pokemonbattle.ru/trainer/{os.getenv('TRAINER_ID')}")
    expect(page.get_by_role("link", name=f"ID {os.getenv('TRAINER_ID')} логотип")).to_be_visible()
    # переход на страницу тренера
    page.get_by_role("link", name=f"ID {os.getenv('TRAINER_ID')} логотип").click()
    page.wait_for_url(f"https://pokemonbattle.ru/trainer/{os.getenv('TRAINER_ID')}")
    # переход со страницы тренера в раздел покупки Премиума
    expect(page.get_by_text("Pokemon Premium", exact=True)).to_be_visible()
    page.locator('[data-qa="premium"]').click()
    page.wait_for_url("https://pokemonbattle.ru/premium")


# 3. проверка активности ачивки «Начало большого пути»
def test_check_achievement(authorized_page):
    page = authorized_page
    page.goto(f"https://pokemonbattle.ru/trainer/{os.getenv('TRAINER_ID')}")
    expect(page.get_by_role("link", name=f"ID {os.getenv('TRAINER_ID')} логотип")).to_be_visible()
    page.get_by_role("link", name=f"ID {os.getenv('TRAINER_ID')} логотип").click()
    page.wait_for_url(f"https://pokemonbattle.ru/trainer/{os.getenv('TRAINER_ID')}")
    expect(page.locator("#beginning")).to_have_class(re.compile(r"\bactive\b"))


# 4. Покупка Премиум
def test_buy_premium(authorized_page, premium_disabled):
    page = authorized_page
    page.goto("https://pokemonbattle.ru/premium")
    page.wait_for_url("https://pokemonbattle.ru/premium")
    page.get_by_placeholder(" ").fill(TEST_CARD["days"])
    expect(page.get_by_role("button", name="Перейти к оплате")).to_be_enabled(timeout=5000)
    page.get_by_role("button", name="Перейти к оплате").click()
    page.wait_for_url("https://pokemonbattle.ru/payment/0")
    page.get_by_role("textbox", name="0000 0000 0000").press_sequentially(TEST_CARD["number"], delay=50)
    page.get_by_role("textbox", name="/00").press_sequentially(TEST_CARD["date"], delay=50)
    page.get_by_role("textbox", name="000", exact=True).press_sequentially(TEST_CARD["cvv"], delay=50)
    page.get_by_role("textbox", name="GERMAN DOLNIKOV").press_sequentially(TEST_CARD["name"], delay=50)
    expect(page.get_by_role("button", name="Оплатить")).to_be_enabled(timeout=5000)
    page.get_by_role("button", name="Оплатить").click()
    page.wait_for_url("https://pokemonbattle.ru/payment_3ds")
    page.get_by_role("textbox", name="00000").fill(TEST_CARD["3ds_code"])
    expect(page.get_by_role("button", name="Оплатить")).to_be_enabled(timeout=15000)
    page.get_by_role("button", name="Оплатить").click()
    page.wait_for_url("https://pokemonbattle.ru/payment_success")
    expect(page.get_by_role("heading", name="Покупка прошла успешно")).to_be_visible()
    me = requests.get(os.getenv("POKEMON_URL") + "/v2/me",
                      headers={"trainer_token": os.getenv("POKEMONBATTLE_TOKEN")})
    body = me.json()
    assert body["data"][0]["is_premium"] is True


# 5. Отмена Премиум
def test_cancel_premium(authorized_page, premium_enabled):
    page = authorized_page
    page.goto("https://pokemonbattle.ru/premium")
    page.wait_for_url("https://pokemonbattle.ru/premium")
    expect(page.get_by_text("Премиум подключен!")).to_be_visible()
    expect(page.get_by_role("button", name="Отменить подписку")).to_be_enabled(timeout=5000)
    page.get_by_role("button", name="Отменить подписку").click()
    page.wait_for_url("https://pokemonbattle.ru/premium")
    expect(page.get_by_text("Вы уверены, что хотите отменить подписку?")).to_be_visible()
    expect(page.get_by_role("button", name="Отменить подписку")).to_be_enabled(timeout=5000)
    page.get_by_role("button", name="Отменить подписку").click()
    expect(page.get_by_text("Вы отменили подписку :(")).to_be_visible()
    me = requests.get(os.getenv("POKEMON_URL") + "/v2/me",
                      headers={"trainer_token": os.getenv("POKEMONBATTLE_TOKEN")})
    body = me.json()
    assert body["data"][0]["is_premium"] is False
