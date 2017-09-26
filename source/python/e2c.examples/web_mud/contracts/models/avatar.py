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

class Race(object):
    races = [
        ('1', 'Mensch'),
        ('2', 'Zauberer'),
        ('3', 'Dunkelelf'),
        ('4', 'Zwerg'),
        ('5', 'Goblin'),
        ('6', 'Ork'),
    ]


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


class Avatar(Creature):
    def __init__(self, entity):
        super(Avatar, self).__init__(entity)
        self.password = entity.password
