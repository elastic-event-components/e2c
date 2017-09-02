from .inventory import Inventory
from .sex import Sex


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
        self.inventory = Inventory()
        self.skills = []
        self.encumberance = 0
        self.char_class = None
        self.level = 1
        self.hp = 0
        self.sp = 0
        self.ep = 0
        self.xp = 0

    @property
    def title(self):
        self.name or self.DEFAULT_NAME

    def he_or_she(self):
        return 'er' if self.sex == 'male' else 'sie'

    def her_or_his(self):
        return 'sein(e)' if self.sex == Sex.male else 'ihr(e)'


# ======================================================= #
# AVATAR OBJECT
# ======================================================= #


class Avatar(Creature):
    def __init__(self, entity):
        super(Avatar, self).__init__(entity)
        self.password = entity.password
        self.char_class = None


# ======================================================= #
# AVATAR OBJECT
# ======================================================= #


class Guest(Creature):
    anonymous = True
    GUEST = 'Gast'

    class ObjectView(object):
        def __init__(self, d):
            self.__dict__ = d

    def __init__(self):
        entity = self.ObjectView({
            'id': None,
            'name': self.GUEST,
            'password': None,
            'race': Creature.DEFAULT_RACE,
            'guild': Creature.DEFAULT_GUILD,
            'position': Creature.DEFAULT_POSITION,
            'sex': None})
        super(Guest, self).__init__(entity)
        self.char_class = None
