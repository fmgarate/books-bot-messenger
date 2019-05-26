class Error(Exception):
    pass


class BotError(Error):
    pass


class PayloadError(BotError):
    pass


class ClientError(BotError):
    pass


class SearchError(BotError):
    pass


class BookError(BotError):
    pass
