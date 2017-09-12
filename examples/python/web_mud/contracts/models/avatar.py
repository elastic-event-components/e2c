# ======================================================= #
# RACE OBJECT
# ======================================================= #

class Race(object):
    races = [
        ('1', 'Mensch'),
        ('2', 'Zauberer'),
        ('3', 'Dunkelelf'),
        ('4', 'Zwerg'),
        ('5', 'Goblin'),
        ('6', 'Ork'),
    ]


# ======================================================= #
# CREATURE OBJECT
# ======================================================= #

class Creature(object):
    anonymous = False

    DEFAULT_RACE = 'Mensch'
    DEFAULT_GUILD = 'Abenteurer'
    DEFAULT_NAME = 'Anonymous'
    DEFAULT_POSITION = 1

    def __init__(self, entity):
        self.id = entity.id
        self.name = entity.name
        self.race = entity.race
        self.guild = entity.guild or self.DEFAULT_GUILD
        self.position = entity.position or self.DEFAULT_POSITION
        self.category = entity.category
        self.topic = entity.topic

        self.sex = entity.sex


    @property
    def title(self):
        return self.name or self.DEFAULT_NAME


# ======================================================= #
# AVATAR OBJECT
# ======================================================= #


class Avatar(Creature):
    def __init__(self, entity):
        super(Avatar, self).__init__(entity)
        self.password = entity.password
