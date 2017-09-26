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

from typing import Callable, Dict

from contracts.models import Avatar
from contracts.token import FToken


def get_by_id(avatar_id: str) -> Avatar:
    from ..repository import AvatarModel
    try:
        try:
            entity = AvatarModel.get(AvatarModel.id == avatar_id)
            return Avatar(entity)
        except AvatarModel.DoesNotExist as e:
            return None
    except Exception as ex:
        raise Exception(FToken.wrap("Der Avatar mit der ID %s existiert nicht" % avatar_id, FToken.error))


def get_by_name(name: str) -> Avatar:
    from ..repository import AvatarModel
    try:
        name = name.strip().title()
        entity = AvatarModel.get(AvatarModel.name == name)
        return Avatar(entity)
    except AvatarModel.DoesNotExist as e:
        raise Exception(FToken.wrap("Avatar %s existiert nicht" % name, FToken.error))


def store_name(
        name: str,
        stored: Callable[[str], None],
        set_avatar_id: Callable[[int], None],
        out: Callable[[str], None]):
    from ..repository import AvatarModel
    name = name.strip().title()
    try:
        AvatarModel.get(AvatarModel.name == name)
        raise Exception(FToken.wrap("Ein Avatar mit dem Namen %s existiert bereits.<br><br>" % name, FToken.error))
    except AvatarModel.DoesNotExist as e:
        avatar = Avatar(AvatarModel.create(
            name=name, race=Avatar.DEFAULT_RACE, guild=Avatar.DEFAULT_GUILD))
        set_avatar_id(avatar.id)
        out('Ein Avatar mit den Namen %s wurde erstellt...<br><br>' % name)
        stored('')


def store_password(
        password: str,
        get_avatar_id: Callable[[None], None],
        stored: Callable[[str], None],
        out: Callable[[str], None]):
    from ..repository import AvatarModel
    try:
        avatar = AvatarModel.get(AvatarModel.id == get_avatar_id())
        avatar.password = password
        AvatarModel.save(avatar)
        out('Password wurde festgelegt.<br><br>')
        stored('')
    except AvatarModel.DoesNotExist as e:
        raise Exception(FToken.wrap("Der Avatar konnte nicht gefunden werden.<br><br>", FToken.error))


def store_race(
        race: str,
        get_avatar_id: Callable[[None], None],
        stored: Callable[[str], None],
        out: Callable[[str], None]):
    from ..repository import AvatarModel
    try:
        avatar = AvatarModel.get(AvatarModel.id == get_avatar_id())
        avatar.race = race
        AvatarModel.save(avatar)
        out('Die Rasse wurde festgelegt.<br><br>')
        stored('')
    except AvatarModel.DoesNotExist as e:
        raise Exception("Der Avatar konnte nicht gefunden werden.<br><br>")


def store_sex(
        sex: str,
        stored: Callable[[str], None],
        get_avatar_id: Callable[[None], None],
        out: Callable[[str], None]):
    from ..repository import AvatarModel
    try:
        avatar = AvatarModel.get(AvatarModel.id == get_avatar_id())
        avatar.sex = sex
        AvatarModel.save(avatar)
        out('%s wurde festgelegt.<br><br>' % sex.title())
        stored('')
    except AvatarModel.DoesNotExist as e:
        raise Exception(FToken.wrap("Der Avatar konnte nicht gefunden werden.<br><br>", FToken.error))


def update(avatar: Avatar, data: Dict, out:Callable[[str], None]) -> None:
    from ..repository import AvatarModel
    if not avatar.anonymous:
        entity = AvatarModel.update(**data).where(AvatarModel.id == avatar.id)
        entity.execute()
    out('')
