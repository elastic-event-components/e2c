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


class Room(object):
    """ Represents the room.
    """

    DIRECTIONS = ["n", "no", "o", "so", "s", "sw", "w", "nw", "ob", "u", "l", 'r']
    DEFAULT_EXITS = dict(zip(DIRECTIONS, [None] * len(DIRECTIONS)))
    DIRECTION_REVERSE = {
        "n": "s", "s": "n",
        "w": "o", "o": "w",
        "nw": "so", "so": "nw",
        "no": "sw", "sw": "no",
        "l": "r", "r": "l",
        "ob": "u", "u": "ob"
    }

    # https://www.key-shortcut.com/schriftsysteme/35-symbole/pfeile/
    DIRECTION_NAMES = dict(zip(DIRECTIONS, [
        "(⇑) <key>N</key>orden", "(⇗) <key>N</key>ord<key>o</key>st",
        "(⇒) <key>O</key>sten", "(⇘) <key>S</key>üd<key>o</key>st",
        "(⇓) <key>S</key>üden", "(⇙) <key>S</key>üd<key>w</key>est",
        "(⇐) <key>W</key>esten", "(⇖) <key>N</key>ordwest",
        "(↥) <key>Ob</key>en", "(↧) <key>U</key>nten",
        "(⇐) <key>L</key>inks", "(⇒) <key>R</key>echts"]))

    def __init__(self, entity):
        self.id = entity.id
        self.name = entity.name or "Raum {}".format(self.id)
        self.description = entity.desc or ""
        self.zone = entity.zone or ""

    @staticmethod
    def get_direction_name(direction, invert=False):
        direction = Room.DIRECTION_REVERSE[direction] if invert else direction
        return Room.DIRECTION_NAMES[direction]
