# ======================================================= #
# ROOM OBJECT
# ======================================================= #


class Room(object):
    """ Represents the room.
    """

    DIRECTIONS = ["n", "no", "o", "so", "s", "sw", "w", "nw", "ob", "u"]
    DEFAULT_EXITS = dict(zip(DIRECTIONS, [None] * len(DIRECTIONS)))
    DIRECTION_REVERSE = {
        "n": "s", "s": "n",
        "w": "o", "o": "w",
        "nw": "so", "so": "nw",
        "no": "sw", "sw": "no",
        "links": "rechts", "rechts": "links",
        "ob": "u", "u": "ob"
    }

    # https://www.key-shortcut.com/schriftsysteme/35-symbole/pfeile/
    DIRECTION_NAMES = dict(zip(DIRECTIONS, [
        "(⇑) Norden", "(⇗) Nordost", "(⇒) Osten", "(⇘) Südost",
        "(⇓) Süden", "(⇙) Südwest", "(⇐) Westen", "(⇖) Nordwest",
        "(↥) Oben", "(↧) Unten"]))

    def __init__(self, entity):
        self.id = entity.id
        self.name = entity.name or "Raum {}".format(self.id)
        self.description = entity.desc or ""
        self.zone = entity.zone or ""
        self.occupants = {}

        # self.terrain = self.TERRAIN[terrain]
        # self.texture = texture
        # self.altitude = altitude
        # self.smell = smell
        # self.sound = sound
        # self.taste = taste

    @staticmethod
    def get_direction_name(direction, invert=False):
        """Returns the full name of a cardinal direction
        """
        direction = Room.DIRECTION_REVERSE[direction] if invert else direction
        return Room.DIRECTION_NAMES[direction]
