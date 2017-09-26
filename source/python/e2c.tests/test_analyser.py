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

import pytest
from e2c import errors
from e2c.analyser import Analyser
from e2c.actor import Actor
from e2c.session import Session


def test_analyser__error_on_no_actor():
    session = Session()
    analyser = Analyser({'A': Actor(session, "A", None)})
    with pytest.raises(errors.E2CAnalyserError) as info:
        analyser.run(quiet=True)
   
    assert str(info.value) == 'Actor A has no callable function!'


def test_analyser__error_on_actor_not_callable():
    session = Session()
    analyser = Analyser({'A': Actor(session, "A", 'xxx')})
    with pytest.raises(errors.E2CAnalyserError) as info:
        analyser.run(quiet=False)
  
    assert str(info.value) == 'Actor A is not a callable function!'


def test_analyser__error_on_actor_invalid_parameter():
    session = Session()
    actor_a = Actor(session, "A", lambda x: None)
    actor_a.on('b', Actor(session, "B", lambda: None))
    analyser = Analyser({'A': actor_a})
    with pytest.raises(errors.E2CAnalyserError) as info:
        analyser.run(quiet=False)
   
    assert str(info.value) == 'b on actor A is not a parameter in the callable function!'
