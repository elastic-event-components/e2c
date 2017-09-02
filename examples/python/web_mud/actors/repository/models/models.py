from typing import Callable
from peewee import *


# ======================================================= #
# DATABASE
# ======================================================= #

db = SqliteDatabase("models.db")


# ======================================================= #
# AVATAR MODEL
# ======================================================= #

class AvatarModel(Model):
    """ The avatar item.
    """

    id = PrimaryKeyField()
    name = CharField()
    sex = CharField(null=True)
    race = CharField(null=True)
    guild = CharField(null=True)
    position = IntegerField(default=1)
    category = IntegerField(null=True)
    topic = IntegerField(null=True)

    password = CharField(null=True)
    email = CharField(null=True)

    class Meta:
        database = db
        db_table = "avatar"


# ======================================================= #
# BOT MODEL
# ======================================================= #

class BotModel(Model):
    """ The bot model.
    """

    id = PrimaryKeyField()
    name = CharField()

    class Meta:
        database = db
        db_table = "bot"


# ======================================================= #
# BOT ACTION MODEL
# ======================================================= #

class BotActionModel(Model):
    """ The bot model.
    """

    id = PrimaryKeyField()
    bot_id = IntegerField()
    pattern = CharField()

    class Meta:
        database = db
        db_table = "bot_action"


# ======================================================= #
# INVENTORY INIT MODEL
# ======================================================= #


class InventoryInitModel(Model):
    """ The item.
    """

    id = PrimaryKeyField()
    key = IntegerField()

    class Meta:
        database = db
        db_table = "inventory_init"


# ======================================================= #
# INVENTORY AVATAR MODEL
# ======================================================= #

class InventoryAvatarModel(Model):
    """ The item.
    """

    id = PrimaryKeyField()
    key = IntegerField()
    avatar = IntegerField()

    class Meta:
        database = db
        db_table = "inventory_avatar"


# ======================================================= #
# ITEM MODEL
# ======================================================= #

class ItemModel(Model):
    """ The item.
    """

    id = PrimaryKeyField()
    name = CharField()
    desc = CharField(null=True)
    tags = CharField(null=True)

    class Meta:
        database = db
        db_table = "item"


# ======================================================= #
# ROOM MODEL
# ======================================================= #

class RoomModel(Model):
    """ The Room.
    """

    id = PrimaryKeyField()
    name = CharField()
    avatar = IntegerField()
    desc = CharField(null=True)
    zone = CharField(null=True)

    class Meta:
        database = db
        db_table = "room"


# ======================================================= #
# ROOM ITEM MODEL
# ======================================================= #

class RoomItemModel(Model):
    """ The item in rooms
    """

    id = PrimaryKeyField()
    room_id = IntegerField()
    item_id = IntegerField()

    class Meta:
        database = db
        db_table = "room_item"


# ======================================================= #
# ROOM EXIT MODEL
# ======================================================= #

class RoomExitModel(Model):
    """ The item in rooms
    """

    id = PrimaryKeyField()
    name = CharField(null=True)
    room_id = IntegerField()
    target_id = IntegerField()
    direct = CharField()

    class Meta:
        database = db
        db_table = "room_exit"


# ======================================================= #
# CONNECT FUNCTION TO BUILD THE DATABASE
# ======================================================= #

def connect_database():
    try:
        db.connect()
        db.create_tables([
            AvatarModel,
            BotModel,
            BotActionModel,
            RoomModel,
            RoomExitModel,
            RoomItemModel,
            ItemModel,
            InventoryInitModel,
            InventoryAvatarModel
        ], safe=True)
    except Exception as exc:
        raise exc


connect_database()