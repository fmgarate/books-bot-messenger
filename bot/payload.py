from .errors import PayloadError


class BotPayload(object):
    def __init__(self, data):
        entry = data.get("entry")
        try:
            assert isinstance(entry, list)
        except AssertionError:
            entry = []
        self._entry = entry

    def __iter__(self):
        for entry in self._entry:
            try:
                messaging = entry["messaging"]
            except KeyError:
                continue
            for data in messaging:
                try:
                    yield BotEvent.create(data)
                except PayloadError:
                    pass


class BotEvent(object):
    def __init__(self, data):
        try:
            self.sender_id = data["sender"]["id"]
        except (TypeError, KeyError):
            raise PayloadError

    @classmethod
    def create(cls, data):
        if "message" in data:
            return MessageEvent(data)
        elif "postback" in data:
            return PostbackEvent(data)
        raise PayloadError


class MessageEvent(BotEvent):
    def __init__(self, data):
        super().__init__(data)
        try:
            self.text = data["message"]["text"]
        except (TypeError, KeyError):
            raise PayloadError

    def handle(self, bot):
        bot.handle_message(self)


class PostbackEvent(BotEvent):
    def __init__(self, data):
        super().__init__(data)
        try:
            self.payload = data["postback"]["payload"]
        except (TypeError, KeyError):
            raise PayloadError
        if "/" in self.payload:
            self.payload, self.ref = self.payload.split("/", 1)

    def handle(self, bot):
        bot.handle_postback(self)
