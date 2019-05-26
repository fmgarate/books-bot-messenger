import re
import requests

from bot.clients import GoodreadsApiClient as BooksClient
from bot.clients import MessengerApiClient as MessagesClient


TEST_SENDER_ID = "PSID_1"
TEST_RECIPIENT_ID = "PAGE_1"


def build_request_payload(event_type, payload):
    return {
        "object": "page",
        "entry": [
            {
                "id": TEST_RECIPIENT_ID,
                "messaging": [
                    {"sender": {"id": TEST_SENDER_ID}, "recipient": {"id": TEST_RECIPIENT_ID}, event_type: payload}
                ],
            }
        ],
    }


def build_message_payload(payload):
    return build_request_payload("message", payload)


def build_postback_payload(payload):
    return build_request_payload("postback", payload)


def test_started_postback(bot, requests_mock):
    """
    Check GET_STARTED postback request and bot response
    """

    adapter = requests_mock.post(MessagesClient.API_URL)
    payload = build_postback_payload({"payload": "GET_STARTED"})

    bot.message(payload)

    assert adapter.called
    assert adapter.call_count == 1
    assert adapter.last_request.json() == {
        "recipient": {"id": TEST_SENDER_ID},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": "Do you want to search for books by id or by name?",
                    "buttons": [
                        {"type": "postback", "title": "By ID", "payload": "SEARCH_BY_ID"},
                        {"type": "postback", "title": "By Name", "payload": "SEARCH_BY_NAME"},
                    ],
                },
            }
        },
    }


def test_search_by_id_postback(bot, requests_mock):
    """
    Check SEARCH_BY_ID postback request and bot response
    """

    adapter = requests_mock.post(MessagesClient.API_URL)
    payload = build_postback_payload({"payload": "SEARCH_BY_ID"})

    bot.message(payload)

    assert adapter.called
    assert adapter.call_count == 1
    assert adapter.last_request.json() == {
        "recipient": {"id": TEST_SENDER_ID},
        "message": {"text": "What is the book ID?"},
    }


def test_search_by_name_postback(bot, requests_mock):
    """
    Check SEARCH_BY_NAME postback request and bot response
    """

    adapter = requests_mock.post(MessagesClient.API_URL)
    payload = build_postback_payload({"payload": "SEARCH_BY_NAME"})

    bot.message(payload)

    assert adapter.called
    assert adapter.call_count == 1
    assert adapter.last_request.json() == {
        "recipient": {"id": TEST_SENDER_ID},
        "message": {"text": "What is the name of the book?"},
    }


def test_fallback_postback(bot, requests_mock):
    """
    Check unknown postback request and bot response
    """

    adapter = requests_mock.post(MessagesClient.API_URL)
    payload = build_postback_payload({"payload": ""})

    bot.message(payload)

    assert adapter.called
    assert adapter.call_count == 1
    assert adapter.last_request.json() == {
        "recipient": {"id": TEST_SENDER_ID},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": "I'm not sure what to do, so, do you want to search for books by id or by name?",
                    "buttons": [
                        {"type": "postback", "title": "By ID", "payload": "SEARCH_BY_ID"},
                        {"type": "postback", "title": "By Name", "payload": "SEARCH_BY_NAME"},
                    ],
                },
            }
        },
    }


def test_fallback_mesagge(bot, requests_mock):

    adapter = requests_mock.post(MessagesClient.API_URL)
    payload = build_message_payload({"text": "Hello"})

    bot.message(payload)

    assert adapter.called
    assert adapter.call_count == 1
    assert (
        adapter.last_request.json()["message"]["attachment"]["payload"]["text"]
        == "I'm not sure what to do, so, do you want to search for books by id or by name?"
    )


def test_search_by_id_messsage(bot, requests_mock, search_results):

    bot.session.search_by_id.return_value = True

    message_adapter = requests_mock.post(MessagesClient.API_URL)
    search_adapter = requests_mock.get(BooksClient.API_SEARCH_URL, text=search_results, complete_qs=False)
    payload = build_message_payload({"text": "Test Book"})

    bot.message(payload)

    assert message_adapter.called
    assert message_adapter.call_count == 1
    assert search_adapter.called
    assert search_adapter.call_count == 1


def test_search_by_name_messsage(bot, requests_mock, search_results):

    bot.session.search_by_name.return_value = True

    message_adapter = requests_mock.post(MessagesClient.API_URL)
    search_adapter = requests_mock.get(BooksClient.API_SEARCH_URL, text=search_results, complete_qs=False)
    payload = build_message_payload({"text": "Test Book"})

    bot.message(payload)

    assert message_adapter.called
    assert message_adapter.call_count == 1
    assert search_adapter.called
    assert search_adapter.call_count == 1


def test_search_error(bot, requests_mock):

    bot.session.search_by_name.return_value = True

    message_adapter = requests_mock.post(MessagesClient.API_URL)
    search_adapter = requests_mock.get(
        BooksClient.API_SEARCH_URL, exc=requests.exceptions.ConnectTimeout, complete_qs=False
    )
    payload = build_message_payload({"text": "Test Book"})

    bot.message(payload)

    assert message_adapter.called
    assert message_adapter.call_count == 1
    assert search_adapter.called
    assert search_adapter.call_count == 1
    assert message_adapter.last_request.json() == {
        "recipient": {"id": "PSID_1"},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": "Sorry no results found, please try again",
                    "buttons": [
                        {"type": "postback", "title": "By ID", "payload": "SEARCH_BY_ID"},
                        {"type": "postback", "title": "By Name", "payload": "SEARCH_BY_NAME"},
                    ],
                },
            }
        },
    }


def test_fetch_book_reviews(bot, requests_mock, book_details):

    bot.session.search_by_name.return_value = True

    matcher = re.compile(BooksClient.API_BASE_URL)

    message_adapter = requests_mock.post(MessagesClient.API_URL)
    search_adapter = requests_mock.get(matcher, text=book_details, complete_qs=False)
    payload = build_postback_payload({"payload": "FETCH_BOOK_REVIEWS/1"})

    bot.message(payload)

    assert message_adapter.called
    assert message_adapter.call_count == 1
    assert search_adapter.called
    assert search_adapter.call_count == 1


def test_fetch_book_reviews_error(bot, requests_mock):

    bot.session.search_by_name.return_value = True

    matcher = re.compile(BooksClient.API_BASE_URL)

    message_adapter = requests_mock.post(MessagesClient.API_URL)
    search_adapter = requests_mock.get(matcher, exc=requests.exceptions.ConnectTimeout, complete_qs=False)
    payload = build_postback_payload({"payload": "FETCH_BOOK_REVIEWS/1"})

    bot.message(payload)

    assert message_adapter.called
    assert message_adapter.call_count == 1
    assert search_adapter.called
    assert search_adapter.call_count == 1
    assert (
        message_adapter.last_request.json()["message"]["attachment"]["payload"]["text"]
        == "Sorry no results found, please try again"
    )


def test_payload_error(bot, requests_mock):
    """
    Check bad request payload, ignore unknown events
    """

    adapter = requests_mock.post(MessagesClient.API_URL)

    # Empty message data
    bot.message({})

    # Empty entry
    bot.message({"object": "page", "entry": None})

    # Missing messaging key
    bot.message({"object": "page", "entry": [{}]})

    # Missing sender and recipient ids
    bot.message({"object": "page", "entry": [{"messaging": [{}]}]})
    bot.message({"object": "page", "entry": [{"messaging": [{"message": {}}]}]})

    # Missing postback and message
    bot.message(
        {
            "object": "page",
            "entry": [
                {
                    "messaging": [
                        {"sender": {"id": TEST_SENDER_ID}, "recipient": {"id": TEST_RECIPIENT_ID}, "postback": None},
                        {"sender": {"id": TEST_SENDER_ID}, "recipient": {"id": TEST_RECIPIENT_ID}, "message": None},
                    ]
                }
            ],
        }
    )

    assert not adapter.called
    assert adapter.call_count == 0
