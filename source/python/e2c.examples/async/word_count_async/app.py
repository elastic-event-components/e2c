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
import asyncio
from os import walk
from typing import Callable

import e2c.async as e2c


async def list_files(dir: str, load_file: Callable[[str], None]):
    for filename in next(walk(dir))[2]:
        await load_file(dir + '/' + filename)


async def open_file(file: str, out: Callable[[str], None]):
    with open(file) as f:
        content = "".join(f.readlines())
    await out(content)


async def word_count(content: str, out: Callable[[str], None]):
    count = len(content.split(' '))
    await out(count)


async def out(dat):
    print('out1', dat)


async def run_async():
    sess = e2c.Session()
    sess.load_graph('app.e2c')

    sess.actor('list_files', list_files)
    sess.actor('open_file', open_file)
    sess.actor('word_count', word_count)
    sess.actor('error', lambda x: print('error', x))
    sess.actor('end', lambda x: print('end'))
    sess.visualize()

    await sess.run_continues('data', out)
    await sess.run_continues('data', lambda out: print('out2', out))


loop = asyncio.get_event_loop()
loop.run_until_complete(run_async())
loop.close()
