from enum import Enum

# ======================================================= #
# FORMATTER TOKEN
# ======================================================= #


class FToken(object):

    intro = 'int'
    broadcast = 'brc'
    text = 'txt'
    enum = 'enum'
    error = 'err'

    room_name = 'rn'
    room_object = 'ro'
    room_desc = 'rd'

    exit_title = 'et'
    exit_object = 'eo'

    item_title = 'it'
    item_object = 'io'

    inv_title = 'ivt'
    inv_object = 'ivo'

    occ_title = 'ot'
    occ_object = 'oo'

    line = '<hr>'

    @staticmethod
    def wrap(text, token):
        return "<%s>%s</%s>" % (token, text, token)

