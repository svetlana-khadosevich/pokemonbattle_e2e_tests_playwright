import os
import pytest
from playwright.sync_api import Page


@pytest.fixture(scope="function")
def authorized_page(page: Page):
    page.goto("https://pokemonbattle.ru/login")
    page.wait_for_url("https://pokemonbattle.ru/login")
    # Заполняем форму авторизации
    page.get_by_role("textbox", name="Почта").click()
    page.get_by_role("textbox", name="Почта").fill(os.getenv("LOGIN"))
    page.get_by_role("textbox", name="Пароль").click()
    page.get_by_role("textbox", name="Пароль").fill(os.getenv("PASSWORD"))
    page.get_by_role("button", name="Войти").click()
    page.wait_for_url("https://pokemonbattle.ru/")
    return page
