from .room import Room


# ======================================================= #
# EXIT OBJECT
# ======================================================= #

class Exit(object):
    """ Represents the exit.
    """

    def __init__(self, entity):
        self.id = entity.id
        self.name = entity.name or ""
        self.direction = entity.direct

    @property
    def title(self):
        direction = str(Room.DIRECTION_NAMES[self.direction])
        return direction + " - " + self.name
