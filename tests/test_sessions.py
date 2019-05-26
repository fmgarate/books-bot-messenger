from unittest import mock

import pytest

from bot.session import Session


TEST_SENDER_ID = "PSID_1"


@pytest.fixture
def session():
    with mock.patch("bot.session.Redis"):
        return Session()


def test_session(session):
    assert session.search_by_id(TEST_SENDER_ID)
    assert session.search_by_name(TEST_SENDER_ID)
    assert session.reset(TEST_SENDER_ID, "search_by_id") is None
