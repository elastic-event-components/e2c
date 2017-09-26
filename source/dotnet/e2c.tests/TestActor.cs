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
    public class TestActor
    {
        private List<int> data = new List<int>();

        private Actor NewActor(string name, object obj)
        {
            var session = new Session();
            return new Actor(session, name, obj);
        }

        [Fact]
        public void Test_On_ErrorOnEmptyName()
        {
            var actor = NewActor("A", null);
            var exc = Assert.Throws<E2CActorError>(delegate ()
            {
                actor.On("", NewActor("Test", null));
            });
            Assert.Equal("Name cannot be null or empty!", exc.Message);
        }

        [Fact]
        public void Test_On_ErrorOnNullName()
        {
            var actor = NewActor("A", null);
            var exc = Assert.Throws<E2CActorError>(delegate ()
            {
                actor.On(null, NewActor("Test", null));
            });
            Assert.Equal("Name cannot be null or empty!", exc.Message);
        }

        [Fact]
        public void Test_On_Name()
        {
            var actor = NewActor("A", null);
            Assert.Equal("A", actor.Name);
        }


        [Fact]
        public void Test_On_DoubleName()
        {
            var actor = NewActor("A", null);
            var childActor1 = NewActor("B", null);
            var childActor2 = NewActor("C", null);
            actor.On("B", childActor1);
            actor.On("B", childActor2);

            Assert.Equal(1, actor.Actors.Keys.Count);
            Assert.Equal(2, actor.Actors["B"].Count);
        }

        [Fact]
        public void Test_Run_ErrorOnNullCallable()
        {
            var actor = NewActor("A", null);
            var exc = Assert.Throws<E2CActorError>(delegate ()
            {
                actor.Run();
            });
            Assert.Equal("Actor A has no callable function!", exc.Message);
        }

        [Fact]
        public void Test_Run_CallAnonymousActor()
        {
            this.data.Clear();
            var actor = NewActor("A", new Action<int>((int x) => { this.data.Add(x); }));

            Assert.Equal(null, actor.Run(1));
            Assert.Equal(1, this.data[0]);
        }

        private void DoCall(int value)
        {
            data.Add(value);
        }

        [Fact]
        public void Test_Run_CallMethodActor()
        {
            this.data.Clear();
            var actor = NewActor("A", new Action<int>(this.DoCall));
            Assert.Equal(null, actor.Run(1));
            Assert.Equal(1, this.data[0]);
        }

        [Fact]
        public void Test_Run_InjectActor()
        {
            var data = new List<Output>();
            var root = NewActor("A", new Action<Output>((Output a) => { data.Add(a); }));
            root.On("a", NewActor("a", new Action(() => { })));
            root.Run();

            Assert.Equal(typeof(Output), data[0].GetType());
        }

        [Fact]
        public void Test_RunWithParams_InjectActor()
        {
            var data = new List<Tuple<int, bool, string>>();
            var root = NewActor("A", new Action<int, bool, string>(
                (int a, bool b, string c) => { data.Add(new Tuple<int, bool, string>(a, b, c)); }));
            var parms = new Object[] { 1, true, "dat" };
            root.RunWithParams(parms);

            Assert.Equal(1, data[0].Item1);
            Assert.Equal(true, data[0].Item2);
            Assert.Equal("dat", data[0].Item3);
        }

        [Fact]
        public void Test_Spec()
        {
            var parms = NewActor(
                "A", new Action<object, string, int, bool, float, List<int>, Dictionary<int, string>>((a, b, c, d, e, f, g) => { })).Specs;

            Assert.Equal(typeof(object), parms["a"]);
            Assert.Equal(typeof(string), parms["b"]);
            Assert.Equal(typeof(int), parms["c"]);
            Assert.Equal(typeof(bool), parms["d"]);
            Assert.Equal(typeof(float), parms["e"]);
            Assert.Equal(typeof(List<int>), parms["f"]);
            Assert.Equal(typeof(Dictionary<int, string>), parms["g"]);
        }

        [Fact]
        public void Test_Clone()
        {
            var actor = new Action<int>((a) => { });

            var cln = NewActor("A", actor);
            cln.On("B", NewActor("B", actor));
            cln.On("C", NewActor("C", actor));
            var clone = cln.Clone();

            Assert.Equal("A", clone.Name);
            Assert.True(clone.callable.Equals(actor));
            Assert.Equal(2, clone.Actors.Count);

            Assert.Equal(1, clone.Actors["B"].Count);
            Assert.True(clone.Actors["B"][0].callable.Equals(actor));
            Assert.True(clone.Actors["C"][0].callable.Equals(actor));
        }

    }
}