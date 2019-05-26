from .clients import GoodreadsApiClient as BooksClient
from .clients import MessengerApiClient as MessagesClient
from .errors import SearchError
from .payload import BotPayload
from .session import Session
from .utils import text, templates as _


class Bot(object):
    def __init__(self, messages=None, books=None, session=None):
        """
        Initializes a bot instance. Messages, Books and Session adapters can be overridden.
        :param messages (object): messages service instance.
        :param books (object): books service instance.
        :param session (object): session service instance.
        """

        self.messages = messages or MessagesClient()
        self.books = books or BooksClient()
        self.session = session or Session()

    def message(self, data):
        """
        Webhook request data, main handler.
        :param data (dict): webhook json data
        """

        payload = BotPayload(data)
        for event in payload:
            event.handle(self)

    def handle_postback(self, event):
        """
        Postback events main handler
        """

        if event.payload == "GET_STARTED":
            self.handle_started_postback(event)
        elif event.payload == "SEARCH_BY_ID":
            self.start_search_by_id(event)
        elif event.payload == "SEARCH_BY_NAME":
            self.start_search_by_name(event)
        elif event.payload == "FETCH_BOOK_REVIEWS":
            self.fetch_book_reviews(event)
        else:
            self.handle_fallback_postback(event)

    def handle_message(self, event):
        """
        Message events main handler
        """

        sender_id = event.sender_id

        if self.session.search_by_id(sender_id):
            self.handle_search_by_id_messsage(event)
        elif self.session.search_by_name(sender_id):
            self.handle_search_by_name_messsage(event)
        else:
            self.handle_fallback_message(event)

    def handle_started_postback(self, event, title=None):
        """
        Started postback event handler
        """

        if title is None:
            title = "Do you want to search for books by id or by name?"

        self.messages.send(
            _.postback_message(event.sender_id, title, (("By ID", "SEARCH_BY_ID"), ("By Name", "SEARCH_BY_NAME")))
        )

    def handle_fallback_postback(self, event):
        self.handle_started_postback(
            event, "I'm not sure what to do, so, do you want to search for books by id or by name?"
        )

    def start_search_by_id(self, event):
        self.session.reset(event.sender_id, "search_by_id")
        self.messages.send(_.message(event.sender_id, "What is the book ID?"))

    def start_search_by_name(self, event):
        self.session.reset(event.sender_id, "search_by_name")
        self.messages.send(_.message(event.sender_id, "What is the name of the book?"))

    def send_search_results(self, event, results):
        self.messages.send(
            _.compact_list(
                event.sender_id,
                (
                    (
                        book.title,
                        book.author,
                        (_.postback_button(f"Describe, {book.title}", f"FETCH_BOOK_REVIEWS/{book.id}"),),
                    )
                    for book in results
                ),
            )
        )

    def handle_search_message(self, event):
        """
        Goodreads search API call
        """

        try:
            results = list(self.books.search(event.text))
        except SearchError:
            results = []

        if results:
            self.send_search_results(event, results)
        else:
            self.handle_started_postback(event, "Sorry no results found, please try again")

    def handle_search_by_id_messsage(self, event):
        self.session.reset(event.sender_id)
        self.handle_search_message(event)

    def handle_search_by_name_messsage(self, event):
        self.session.reset(event.sender_id)
        self.handle_search_message(event)

    def handle_fallback_message(self, event):
        self.session.reset(event.sender_id)
        self.handle_fallback_postback(event)

    def fetch_book_reviews(self, event):
        """
        Book reviews main handler. Gets a review from books API and returns a description.
        """

        self.session.reset(event.sender_id)

        try:
            description = self.books.get_description(event.ref)
        except SearchError:
            description = None

        # TODO: analyze the book's description and create a recommendation.
        if description:
            short_description = text.strip_tags(description)[:2000]
            self.messages.send(_.message(event.sender_id, short_description))
        else:
            self.handle_started_postback(event, "Sorry no results found, please try again")
