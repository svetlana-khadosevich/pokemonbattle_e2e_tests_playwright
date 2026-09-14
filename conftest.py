import os

import pytest
from dotenv import load_dotenv

pytest_plugins = [
    "fixtures.api_fixtures",
    "fixtures.ui_fixtures"
]


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="session")
def launch_browser_args():
    return {
        "headless": False,
        "slow_mo": int(os.getenv("SLOW_MO", 0)),
    }


@pytest.fixture(scope="session")
def browser_context_args():
    return {
        "viewport": {"width": 1440, "height": 900}
    }


@pytest.fixture
def page(page):  # переопределяем стандартную фикстуру
    page.set_default_timeout(10000)
    page.set_default_navigation_timeout(15000)
    return page


@pytest.fixture(scope="session", autouse=True)
def _set_test_id_attribute(playwright):
    playwright.selectors.set_test_id_attribute("data-id")
