def selector_as_string(selector):
    if len(selector) >= 1:
        return '.'.join(selector)
    else:
        return '.'


def dummy_gettext(msg):
    return msg
