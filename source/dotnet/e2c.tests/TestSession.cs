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
using System.IO;
using Xunit;
using E2c;
using System.Collections.Generic;
using System.Reflection;
using System.Text;

namespace E2c.Tests
{
    class MockAnalyser : Analyser
    {
        public bool Quite;
        public MockAnalyser() : base(null) { }
        public override void Run(bool quite = true)
        {
            this.Quite = quite;
        }
    }

    class MockVisualizer : Visualizer
    {
        public string Name;
        public string Folder;
        public MockVisualizer() : base(null) { }
        public override void Run(string folder, string name)
        {
            this.Folder = folder;
            this.Name = name;
        }
    }

    class MockableSession : Session
    {
        public new void Init(
            Dictionary<string, Actor> actors, Analyser analyser,
            Parser parser, Visualizer visualizer, string[] script)
        {
            // Method is protected.
            base.Init(actors, analyser, parser, visualizer, script);
        }

    }

    public class TestSession
    {
        private string GetGraphFile(string filename)
        {
            var codeBaseUrl = new Uri(Assembly.GetExecutingAssembly().CodeBase);
            var codeBasePath = Uri.UnescapeDataString(codeBaseUrl.AbsolutePath);
            var dirPath = Path.GetDirectoryName(codeBasePath);
            return Path.Combine(dirPath, "..", "..", "..", "graph", filename);
        }

        [Fact]
        public void Test_Analyse()
        {
            var mockup = new MockAnalyser();
            var session = new MockableSession();
            session.Init(new Dictionary<string, Actor> { }, mockup, null, null, null);
            session.Analyse(quite: true);

            Assert.Equal(true, mockup.Quite);
        }

        [Fact]
        public void Test_Visualize()
        {
            var mockup = new MockVisualizer();
            var session = new MockableSession();
            session.Init(new Dictionary<string, Actor> { }, null, null, mockup, null);
            session.Name = "Test";
            session.Visualize("TestFolder");

            Assert.Equal("TestFolder", mockup.Folder);
            Assert.Equal(session.Name, mockup.Name);
        }

        [Fact]
        public void Test_Actor_ErrorOnDoubleName()
        {
            var session = new Session();
            session.Actor("A", new Action(() => { }));
            var exc = Assert.Throws<E2CSessionError>(delegate ()
            {
                session.Actor("A", new Action(() => { }));
            });

            Assert.Equal("Actor A was already registered!", exc.Message);
        }

        [Fact]
        public void Test_ParseGraph_ErrorOnEmptyGraph()
        {
            var exc = Assert.Throws<E2CParserError>(delegate ()
            {
                new Session(new String[] { "" });
            });

            Assert.Equal("No data to parse!", exc.Message);
        }

        [Fact]
        public void Test_ParseGraph_ErrorOnMisingDoubleLine()
        {
            var exc = Assert.Throws<E2CParserError>(delegate ()
            {
                new Session(new String[] { ".run", "" });
            });

            Assert.Equal("Missing -- in line 1!", exc.Message);
        }

        [Fact]
        public void Test_ParseGraph_ErrorOnMisingTarget()
        {
            var exc = Assert.Throws<E2CParserError>(delegate ()
            {
                new Session(new String[] { ".run --", "" });
            });

            Assert.Equal("Missing actor in line 1!", exc.Message);
        }

        [Fact]
        public void Test_LoadGraph_ErrorOnInvalidFilenName()
        {
            var session = new Session();
            var exc = Assert.Throws<E2CSessionError>(delegate ()
            {
                session.LoadGraph("graph/xxx.e2c");
            });
        }

        [Fact]
        public void Test_Run_ThrowCustomException()
        {
            var config = new String[] { ".run -- A" };
            var session = new Session(config);
            session.Actor("A", new Action(() => { throw new Exception("xxx"); }));
            var exc = Assert.Throws<Exception>(delegate ()
            {
                session.Run<object, object>();
            });

            Assert.Equal("xxx", exc.Message);
        }

        [Fact]
        public void Test_Run_ThrowExceptionMissingRun()
        {
            var config = new String[] { ".trace -- Trace" };
            var session = new Session(config);
            session.Actor("Trace", new Action(() => { }));
            var exc = Assert.Throws<E2CSessionError>(delegate ()
            {
                session.Run<object, object>();
            });

            Assert.Equal("Missing .run -- ? in graph!", exc.Message);
        }


        [Fact]
        public void Test_Run_ThrowExceptionCatchError()
        {
            var errors = new List<Exception>();
            var config = new String[] {
                ".err -- Error",
                ".run -- A"  };

            var session = new Session(config);
            session.Actor("A", new Action(() => { throw new ArgumentException("xxx"); }));
            session.Actor("Error", new Action<Exception>((x) => { errors.Add(x); }));
            session.Run<object, object>();

            Assert.Equal("xxx", errors[0].Message);
        }

        [Fact]
        public void Test_Run_AssignBeforeDefine()
        {
            var data = new List<object>();
            var config = new String[] {
                "A.write -- B",
                ".run -- A"  };

            var actor1 = new Action<string, Output<string>>(
                (a, write) => { write.Invoke(a); });

            var session = new Session(config);
            session.Actor("A", actor1);
            session.Actor("B", new Action<object>((x) => { data.Add(x); }));
            session.Run<string, object>("data");

            Assert.Equal("data", data[0]);
        }

        class TestRunClass
        {
            public void Operation(int value, Output<int> output)
            {
                output.Invoke(value + 5);
            }
        }

        [Fact()]
        public void Test_Run()
        {
            var actorB = new Action<int, Output<object>>(
                (value, output) => { output.Invoke(value * 2); });

            var session = new Session();
            session.Actor("A", new TestRunClass(), "Operation");
            session.Actor("B", actorB);
            session.LoadGraph(GetGraphFile("t1.e2c"));

            Assert.Equal(16, session.Run<int, int>(3));
            Assert.Equal(16, session.Run<int, int>(3, actor: "A"));
            Assert.Equal(6, session.Run<int, int>(3, actor: "B"));
            Assert.Equal(14, session.Run<int, int>(2, actor: "A"));
        }

        [Fact()]
        public void Test_Run_ErrorOnInvalidStartActor()
        {
            var actor = new Action<int, Output<object>>(
                (value, output) => { });
            var session = new Session();
            session.Actor("A", actor);
            session.Actor("B", actor);
            session.LoadGraph(GetGraphFile("t1.e2c"));

            var exc = Assert.Throws<E2CSessionError>(delegate ()
            {
                session.Run<int, int>(1, actor: "X");
            });

            Assert.Equal("X is not a registered actor!", exc.Message);
        }

        [Fact()]
        public void Test_Run_CallEnd()
        {
            var actor1 = new Action<int, Output<object>>(
                (value, output) => { output.Invoke(value); });
            var actor2 = new Action<int, Output<object>>(
                (value, output) => { output.Invoke(value + 2); });

            var data = new List<int>();
            var session = new Session();
            session.Actor("A", actor1);
            session.Actor("B", actor2);
            session.Actor("C", new Action<int>((value) => { data.Add(value); }));
            session.LoadGraph(GetGraphFile("t2.e2c"));

            var startValue = 1;
            Assert.Equal(3, session.Run<int, int>(startValue));
            Assert.Equal(startValue, data[0]);
        }

        [Fact()]
        public void Test_Run_CallTrace()
        {
            var actor = new Action<int, Output<object>>(
                (value, output) => { output.Invoke(value); });

            var data = new List<object>();
            var session = new Session();
            session.Actor("A", actor);
            session.Actor("B", actor);
            session.Actor("Trace", new Action<object>((value) => { data.Add(value); }));
            session.LoadGraph(GetGraphFile("t3.e2c"));

            session.Run<object, object>(null);
            Assert.Equal(new object[] { "A", "B" }, data.ToArray());
        }

        [Fact()]
        public void Test_Run_Continues()
        {
            var actor1 = new Action<int, Output<object>>(
                (value, output) => { output.Invoke(value + 1); });
            var actor2 = new Action<int, Output<object>>(
                (value, output) => { output.Invoke(value * 3); });

            var data = new List<object>();
            var session = new Session();
            session.Actor("A", actor1);
            session.Actor("B", actor2);
            session.LoadGraph(GetGraphFile("t4.e2c"));
            session.RunContinues(
                3, new Action<object>((result) => { data.Add(result); }));

            Assert.Equal(new object[] { 12, 12, 12 }, data.ToArray());
        }


    }
}