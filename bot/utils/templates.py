def build_text_message(sender_id, message):
    return {"recipient": {"id": sender_id}, "message": message}


def build_template_message(sender_id, payload):
    return {"recipient": {"id": sender_id}, "message": {"attachment": {"type": "template", "payload": payload}}}


def postback_button(title, payload):
    return {"type": "postback", "title": title, "payload": payload}


def list_item(title, subtitle, buttons):
    return {"title": title, "subtitle": subtitle, "buttons": buttons}


def message(sender_id, text):
    return build_text_message(sender_id, message={"text": text})


def postback_message(sender_id, text, buttons):
    return build_template_message(
        sender_id,
        payload={
            "template_type": "button",
            "text": text,
            "buttons": list(postback_button(title, payload) for title, payload in buttons),
        },
    )


def compact_list(sender_id, elements):
    return build_template_message(
        sender_id,
        payload={
            "template_type": "list",
            "top_element_style": "compact",
            "elements": list(list_item(title, subtitle, buttons) for (title, subtitle, buttons) in elements),
        },
    )
