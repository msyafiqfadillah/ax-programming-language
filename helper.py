from tokens.keywords import Keywords


def is_eof(c_index, data):
    return c_index >= len(data)

def bool_converter(value):
    return Keywords.TRUE if value else Keywords.FALSE

def is_truhty(value):
    return value not in ("", Keywords.FALSE, Keywords.EMPTY, Keywords.UNDEFINED)