#
# Copyright 2017 The E2C Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

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
