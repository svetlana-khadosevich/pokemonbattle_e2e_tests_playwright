import pytest
from pages.login_page import LoginPage
from pages.main_page import MainPage
from playwright.sync_api import Page


@pytest.fixture(scope="function")
def authorized_page(page: Page):
    login_page = LoginPage(page)
    login_page.open_page()
    login_page.should_be_login_page()
    login_page.login()
    main_page = MainPage(page)
    main_page.should_be_main_page()
    return page
