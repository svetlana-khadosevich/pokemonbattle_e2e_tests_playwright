import os

import requests
import pytest


@pytest.fixture(scope="function")
def premium_disabled():
    with requests.Session() as lavka_session:
        lavka_session.headers.update({"trainer_token": os.getenv("POKEMONBATTLE_TOKEN")})
        # отменяем премиум на случай, если он был до выполнения теста
        lavka_session.post(os.getenv("LAVKA_URL") + "/cancel_premium")
        yield lavka_session
        response = lavka_session.post((os.getenv("LAVKA_URL") + "/cancel_premium"))
        assert response.status_code == 200


@pytest.fixture(scope="function")
def premium_enabled():
    with requests.Session() as lavka_session:
        lavka_session.headers.update({"trainer_token": os.getenv("POKEMONBATTLE_TOKEN")})
        lavka_session.post((os.getenv("LAVKA_URL") + "/cancel_premium"))
        response = lavka_session.post((os.getenv("LAVKA_URL") + "/payments"),
                                      json={
                                          "order_type": "premium",
                                          "details":
                                              {
                                                  "card_number": (os.getenv("CARD_NUMBER")),
                                                  "secure_code": (os.getenv("CARD_3DS_CODE")),
                                                  "card_name": (os.getenv("CARD_NAME")),
                                                  "card_cvv": (os.getenv("CARD_CVV")),
                                                  "card_actual": (os.getenv("CARD_DATE")),
                                                  "days": (os.getenv("DAYS"))
                                              }
                                      }
                                      )
        assert response.status_code == 200
