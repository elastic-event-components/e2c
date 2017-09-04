from peewee import *

# ======================================================= #
# DATABASE
# ======================================================= #

db = SqliteDatabase("models.db")


# ======================================================= #
# AVATAR MODEL
# ======================================================= #

class AvatarModel(Model):
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
# ROOM MODEL
# ======================================================= #

class RoomModel(Model):
    id = PrimaryKeyField()
    name = CharField()
    avatar = IntegerField()
    desc = CharField(null=True)
    zone = CharField(null=True)

    class Meta:
        database = db
        db_table = "room"


# ======================================================= #
# EXIT MODEL
# ======================================================= #

class ExitModel(Model):
    id = PrimaryKeyField()
    name = CharField(null=True)
    room_id = IntegerField()
    target_id = IntegerField()
    direct = CharField()

    class Meta:
        database = db
        db_table = "exit"


# ======================================================= #
# CONNECT FUNCTION TO BUILD THE DATABASE
# ======================================================= #

def connect_database():
    try:
        db.connect()
        db.create_tables([
            AvatarModel,
            RoomModel,
            ExitModel,
        ], safe=True)
    except Exception as exc:
        raise exc


connect_database()
