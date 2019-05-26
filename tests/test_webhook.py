import pytest


TEST_VERIFY_TOKEN = "TEST_TOKEN"
TEST_CHALLENGE = "TEST_CHALLENGE"


@pytest.fixture
def app(monkeypatch):
    monkeypatch.setenv("FACEBOOK_VERIFY_TOKEN", TEST_VERIFY_TOKEN)

    import main

    main.app.testing = True
    return main.app.test_client()


def test_webhook_message(app):

    response = app.post("/webhook", json={})

    assert response.status_code == 200
    assert response.data.decode("utf-8") == "OK"


def test_webhook_verification(app):

    response = app.get(
        "/webhook", query_string={"hub.verify_token": TEST_VERIFY_TOKEN, "hub.challenge": TEST_CHALLENGE}
    )

    assert response.status_code == 200
    assert response.data.decode("utf-8") == TEST_CHALLENGE


def test_webhook_verification_error(app):

    response = app.get("/webhook", query_string={})

    assert response.status_code == 200
    assert response.data.decode("utf-8") == "Error, wrong validation token"
