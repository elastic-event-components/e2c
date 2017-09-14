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

from typing import Callable


def run(out: Callable[[str], None]):
    text = (
        'Du schwebst im Nirgendwo. Sterne umgeben Dich, und Du glaubst zu fallen,<br>'
        'obwohl Du Dich vollkommen schwerelos fühlst. Ein hauchdünner Schleier aus<br>'
        'Staub umfängt Dich, als Du langsam aber sicher Deines Körpers gewahr wirst.<br>'
        '<br>'
        'Du schaust Dich erstaunt um. Du befindest Dich anscheinend im Weltall, aber<br>'
        'wie bist Du hierhergekommen? Ist das schon das MorgenGraün, oder bist Du wohl<br>'
        'erst noch auf dem Weg dorthin?<br>'
        '<br>'
        'Mit einem Blick auf Deine Umgebung bemerkst Du, dass der Staub, der Dich<br>'
        'umgibt, sich langsam auf Dich zuzubewegen scheint. Du willst neugierig danach<br>'
        'greifen, aber es will Dir nicht gelingen. Verwundert stellst Du fest, dass Du<br>'
        'keine Hände besitzt, und bei näherer Betrachtung wird Dir klar, dass Du auch<br>'
        'sonst noch ziemlich körperlos bist!<br>'
        '<br>'
        'Das ändert sich aber bald, als der glitzernde Staub allmählich um Dich herum<br>'
        'eine durchscheinende Gestalt zu bilden beginnt, die sich zügig verdichtet.<br>'
        '<br>'
        'Schon kurz darauf hat sich ein eleganter Körper geformt, der nun vollkommen<br>'
        'Dir gehört. Dass Du noch nackt bist, stört Dich nicht im geringsten, denn<br>'
        'endlich, endlich fühlst Du Dich wie ein richtiger Mensch!<br>'
        '<br>'
        'Deine Begeisterung über Deinen makellosen Körper wird jäh unterbrochen, als<br>'
        'plötzlich die Sterne verblassen und sich mit unfassbarem Tempo von Dir zu<br>'
        'entfernen scheinen. Dann wird es kurz schwarz um Dich herum und kurz darauf<br>'
        'wieder hell.<br>'
        '<br>'
        'Drücke eine Taste...')
    out(text)