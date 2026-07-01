from tokens.keywords import Keywords


def is_eof(c_index, data):
    return c_index >= len(data)

def is_truthy(value):
    return value not in ("", Keywords.FALSE, Keywords.EMPTY, Keywords.UNDEFINED)