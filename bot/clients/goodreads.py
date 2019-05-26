import os

import requests
import xmltodict

from bot.errors import ClientError, SearchError, BookError


GOODREADS_KEY = os.getenv("GOODREADS_KEY")


class GoodreadsApiClient(object):

    API_BASE_URL = "https://www.goodreads.com"
    API_SEARCH_URL = "https://www.goodreads.com/search/index.xml"

    def _make_api_request(self, url, params):
        try:
            response = requests.get(url, params=params)
        except requests.RequestException:
            raise ClientError
        try:
            response.raise_for_status()
        except requests.HTTPError:
            raise ClientError
        try:
            return xmltodict.parse(response.content)
        except Exception:
            raise ClientError

    def search(self, query):
        try:
            doc = self._make_api_request(self.API_SEARCH_URL, {"key": GOODREADS_KEY, "q": query})
        except ClientError:
            raise SearchError
        try:
            return GoodreadsSearchResults(doc["GoodreadsResponse"]["search"]["results"]["work"])
        except (TypeError, KeyError):
            raise SearchError

    def get_description(self, book_id):
        url = f"https://www.goodreads.com/book/show/{book_id}.xml"
        try:
            doc = self._make_api_request(url, {"key": GOODREADS_KEY})
        except ClientError:
            raise SearchError
        try:
            return doc["GoodreadsResponse"]["book"]["description"]
        except (TypeError, KeyError):
            raise SearchError


class GoodreadsSearchResults(object):

    _limit = 4

    def __init__(self, results):
        self._results = results

    def __iter__(self):
        valid = 0
        for data in self._results:
            if valid < self._limit:
                try:
                    yield Book(data)
                    valid += 1
                except BookError:
                    pass


class Book(object):
    def __init__(self, data):
        try:
            self.id = data["best_book"]["id"]["#text"]
            self.title = data["best_book"]["title"]
            self.author = data["best_book"]["author"]["name"]
        except (TypeError, KeyError):
            raise BookError
