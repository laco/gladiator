def selector_as_string(selector):
    if len(selector) >= 1:
        return '.'.join([str(s) for s in selector])
    else:
        return '.'


def dummy_gettext(msg):
    return msg
