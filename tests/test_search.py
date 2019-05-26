import re

import pytest
import requests

from bot.clients import GoodreadsApiClient as BooksClient
from bot.errors import SearchError


def test_search_error(requests_mock, bad_search_results):

    failed_responses = (
        {"text": ""},
        {"text": "<xml/>"},
        {"status_code": 404},
        {"exc": requests.exceptions.ConnectTimeout},
    )

    adapter = requests_mock.get(BooksClient.API_SEARCH_URL, failed_responses, complete_qs=False)

    books = BooksClient()

    for _ in failed_responses:
        with pytest.raises(SearchError):
            books.search("Test Term")

    assert adapter.called
    assert adapter.call_count == 4

    adapter = requests_mock.get(BooksClient.API_SEARCH_URL, text=bad_search_results, complete_qs=False)

    results = books.search("Test Term")

    assert len(list(results)) == 0
    assert adapter.called
    assert adapter.call_count == 1


def test_search_book_description_error(requests_mock):

    matcher = re.compile(BooksClient.API_BASE_URL)
    adapter = requests_mock.get(matcher, text="<xml/>", complete_qs=False)

    books = BooksClient()

    with pytest.raises(SearchError):
        books.get_description(1)

    assert adapter.called
    assert adapter.call_count == 1


def test_search(search_results, requests_mock):

    adapter = requests_mock.get(BooksClient.API_SEARCH_URL, text=search_results, complete_qs=False)

    books = BooksClient()
    results = books.search("Test Term")

    assert len(list(results)) == 2

    assert adapter.called
    assert adapter.call_count == 1
