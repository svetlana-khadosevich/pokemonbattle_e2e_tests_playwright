import os

import allure

import requests
import pytest

from tests.data.test_data import TEST_CARD


@pytest.fixture(scope="function")
def buy_premium():
    with requests.Session() as lavka_session:
        lavka_session.headers.update({"trainer_token": os.getenv("POKEMONBATTLE_TOKEN")})
        # отменяем премиум на случай, если он был до выполнения теста
        lavka_session.post(os.getenv("LAVKA_URL") + "/cancel_premium")
        yield lavka_session
        response = lavka_session.post((os.getenv("LAVKA_URL") + "/cancel_premium"))
        assert response.status_code == 200


@pytest.fixture(scope="function")
def cancel_premium():
    with requests.Session() as lavka_session:
        lavka_session.headers.update({"trainer_token": os.getenv("POKEMONBATTLE_TOKEN")})
        lavka_session.post((os.getenv("LAVKA_URL") + "/cancel_premium"))
        response = lavka_session.post((os.getenv("LAVKA_URL") + "/payments"),
                                      json={
                                          "order_type": "premium",
                                          "details":
                                              {
                                                  "card_number": TEST_CARD["number"],
                                                  "secure_code": TEST_CARD["3ds_code"],
                                                  "card_name": TEST_CARD["name"],
                                                  "card_cvv": TEST_CARD["cvv"],
                                                  "card_actual": TEST_CARD["date"],
                                                  "days": TEST_CARD["days"]
                                              }
                                      }
                                      )
        assert response.status_code == 200
