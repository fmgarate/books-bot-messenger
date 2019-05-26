from bot.utils import templates as _


TEST_SENDER_ID = "PSID_1"

BTN_1_TITLE = "Test Button 1"
BTN_1_PAYLOAD = "TEST_BTN_1"
BTN_1 = {"type": "postback", "title": BTN_1_TITLE, "payload": BTN_1_PAYLOAD}

BTN_2_TITLE = "Test Button 2"
BTN_2_PAYLOAD = "TEST_BTN_2"
BTN_2 = {"type": "postback", "title": BTN_2_TITLE, "payload": BTN_2_PAYLOAD}

# build_template_message
# message


def test_build_template_message():
    assert _.build_template_message(TEST_SENDER_ID, {}) == {
        "recipient": {"id": TEST_SENDER_ID},
        "message": {"attachment": {"type": "template", "payload": {}}},
    }


def test_postback_button():
    assert _.postback_button(BTN_1_TITLE, BTN_1_PAYLOAD) == BTN_1


def test_list_item():
    assert _.list_item("Title", "Sub Title", ()) == {"title": "Title", "subtitle": "Sub Title", "buttons": ()}


def test_message():
    assert _.message(TEST_SENDER_ID, "Test Message") == {
        "recipient": {"id": TEST_SENDER_ID},
        "message": {"text": "Test Message"},
    }


def test_postback_message():
    assert _.postback_message(
        TEST_SENDER_ID, "Test Text", [(BTN_1_TITLE, BTN_1_PAYLOAD), (BTN_2_TITLE, BTN_2_PAYLOAD)]
    ) == {
        "recipient": {"id": TEST_SENDER_ID},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {"buttons": [BTN_1, BTN_2], "template_type": "button", "text": "Test Text"},
            }
        },
    }


def test_compact_list():
    assert _.compact_list(
        TEST_SENDER_ID, (("Title 1", "Sub Title 1", (BTN_1,)), ("Title 2", "Sub Title 2", (BTN_2,)))
    ) == {
        "recipient": {"id": "PSID_1"},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "list",
                    "top_element_style": "compact",
                    "elements": [
                        {"title": "Title 1", "subtitle": "Sub Title 1", "buttons": (BTN_1,)},
                        {"title": "Title 2", "subtitle": "Sub Title 2", "buttons": (BTN_2,)},
                    ],
                },
            }
        },
    }
