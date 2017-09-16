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


class E2CAnalyserError(Exception):
    """ The error class to raise exceptions in :class:`e2c.analyser.Analyser`
    """
    pass


class E2CSessionError(Exception):
    """ The error class to raise exceptions in :class:`e2c.session.Session`
    """
    pass


class E2CActorError(Exception):
    """ The error class to raise exceptions in :class:`e2c.actor.Actor`
    """
    pass


class E2CVisualizeError(Exception):
    """ The error class to raise exceptions in :type:`e2c.visualizer.Visualizer`
    """
    pass


class E2CParserError(Exception):
    """ The error class to raise exceptions in :class:`e2c.parser.Parser`
    """
    pass
