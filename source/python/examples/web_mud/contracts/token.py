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


class FToken(object):
    intro = 'int'
    broadcast = 'brc'
    text = 'txt'
    enum = 'enum'
    error = 'err'

    room_name = 'rn'
    room_object = 'ro'
    room_desc = 'rd'

    exit_title = 'et'
    exit_object = 'eo'

    item_title = 'it'
    item_object = 'io'

    inv_title = 'ivt'
    inv_object = 'ivo'

    occ_title = 'ot'
    occ_object = 'oo'

    line = '<hr>'

    @staticmethod
    def wrap(text, token):
        return "<%s>%s</%s>" % (token, text, token)
