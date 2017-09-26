//
// Copyright 2017 The E2C Authors. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// ==============================================================================

using System;
using Xunit;
using E2c;
using System.Collections.Generic;

namespace E2c.Tests
{
    public class TestAnalyser
    {

        [Fact]
        public void Test_Analyser_ErrorOnNoActor()
        {
            var session = new Session();
            var analyser = new Analyser(
                new Dictionary<string, Actor> { { "A", new Actor(session, "A", null) } });
            var exc = Assert.Throws<E2CAnalyserError>(delegate ()
            {
                analyser.Run(quite: true);
            });
            Assert.Equal(exc.Message, "Actor A has no callable function!");
        }

        [Fact]
        public void Test_Analyser_ErrorOnActorNotCallable()
        {
            var session = new Session();
            var analyser = new Analyser(
                new Dictionary<string, Actor> { { "A", new Actor(session, "A", "xxx") } });
            var exc = Assert.Throws<E2CAnalyserError>(delegate ()
            {
                analyser.Run(quite: false);
            });
            Assert.Equal(exc.Message, "Actor A is not a callable function!");
        }

        [Fact]
        public void Test_Analyser_ErrorOnActorInvalidParameter()
        {
            var session = new Session();
            var actorA = new Actor(session, "A", new Action<int>((x) => { }));
            actorA.On("b", new Actor(session, "B", new Action(() => { })));
            var analyser = new Analyser(new Dictionary<string, Actor> { { "A", actorA } });
            var exc = Assert.Throws<E2CAnalyserError>(delegate ()
            {
                analyser.Run(quite: false);
            });
            Assert.Equal(exc.Message, "b on actor A is not a parameter in the callable function!");
        }

    }
}