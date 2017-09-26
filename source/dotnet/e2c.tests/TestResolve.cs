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
    public class TestResolve
    {
        private Actor NewActor(string name, object obj)
        {
            var session = new Session();
            return new Actor(session, name, obj);
        }

        [Fact]
        public void Test_Event_Call()
        {
            var data = new List<string>();
            var actor = NewActor("A", new Action<string>((a) => { data.Add(a); }));
            var output = new Output<string>(actor, null);
            output.Invoke("Hello");
            Assert.Equal(data[0], "Hello");
        }


        [Fact]
        public void Test_Resolve_Value()
        {
            var action = new Action<int, string, bool, object, object>(
                (a, b, c, d, e) => { });

            var actor = NewActor("A", action);
            var result1 = Resolver.Resolve(actor, new object[] { 1, "data", true });
            var result2 = Resolver.Resolve(actor, new object[] { });

            Assert.Equal(5, result1.Length);
            Assert.Equal(new object[] { 1, "data", true, null, null }, result1);
            Assert.Equal(new object[] { null, null, null, null, null }, result2);
        }

    }
}