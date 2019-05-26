from unittest.mock import Mock
import pytest

from bot import Bot


@pytest.fixture
def session():
    session = Mock()
    session.search_by_id = Mock(return_value=False)
    session.search_by_name = Mock(return_value=False)
    return session


@pytest.fixture
def bot(session):
    return Bot(session=session)


@pytest.fixture
def search_results():
    with open("tests/test_search.xml") as fd:
        return fd.read()


@pytest.fixture
def bad_search_results():
    with open("tests/test_search_error.xml") as fd:
        return fd.read()


@pytest.fixture
def book_details():
    with open("tests/test_book.xml") as fd:
        return fd.read()
