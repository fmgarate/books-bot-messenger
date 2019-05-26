import json
import os

import requests


FACEBOOK_PAGE_ACCESS_TOKEN = os.getenv("FACEBOOK_PAGE_ACCESS_TOKEN")


class MessengerApiClient(object):

    API_URL = "https://graph.facebook.com/v2.6/me/messages"

    def send(self, payload):
        requests.post(
            self.API_URL,
            params={"access_token": FACEBOOK_PAGE_ACCESS_TOKEN},
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
        )
