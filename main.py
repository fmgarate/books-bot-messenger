"""
Help readers evaluate books using facebook messenger chatbot.
The conversation should go like this:

- Welcome the user by using their first name
- Ask the user if they want to search for books by name or by ID (Goodreads ID)
- Use Goodreads API to search for books
- Retrieve a maximum of 4 books and let the user select one of them
- Retrieve the selected book's reviews from Goodreads and use IBM Watson to do a
  semantic analysis for the most recent reviews
- Suggest the user if they should buy the book or not based on the
  semantic analysis done in the previous step
"""

import os

from flask import Flask, request
from bot import Bot

app = Flask(__name__)
bot = Bot()


@app.route("/webhook", methods=("POST",))
def handle_message():
    """
    Facebook Messenger messages handler
    """

    bot.message(request.get_json() or {})

    return "OK"


@app.route("/webhook", methods=("GET",))
def handle_verification():
    """
    Facebook webhook url verification
    """

    if request.args.get("hub.verify_token", "") == os.getenv("FACEBOOK_VERIFY_TOKEN"):
        return request.args.get("hub.challenge", "")

    return "Error, wrong validation token"
