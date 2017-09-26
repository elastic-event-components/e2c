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

    public class TestVisualizer
    {
        private string GetGraphFile(string filename)
        {
            var codeBaseUrl = new Uri(Assembly.GetExecutingAssembly().CodeBase);
            var codeBasePath = Uri.UnescapeDataString(codeBaseUrl.AbsolutePath);
            var dirPath = Path.GetDirectoryName(codeBasePath);
            return Path.Combine(dirPath, "..", "..", "..", "graph", filename);
        }

        private string GetTempFolder()
        {
            return Path.Combine(Path.GetTempPath(), "e2c");
        }

        [Fact]
        public void Test_Run_ErrorOnNoConfiguration()
        {
            var session = new Session();
            var rootActor = new Actor(session, Const.SELF, null);

            var folder = GetTempFolder();
            var vis = new Visualizer(new Dictionary<string, Actor> { { Const.SELF, rootActor } });
            var exc = Assert.Throws<E2CVisualizeError>(delegate ()
            {
                vis.Run(folder, "MyName");
            });
            Assert.Equal("Graph is empty!", exc.Message);
        }

 [Fact]
        public void Test_Run_build()
        {
            var session = new Session();
            var rootActor = new Actor(session, Const.SELF, null);
            var actors = new Dictionary<string, Actor>();

            var bActor = new Actor(session, "B", null);
            actors.Add("B", bActor);

            var aActor = new Actor(session, "A", null);
            aActor.On("Write", new Actor(session, Const.OUT, null));
            aActor.On("Write", bActor);
            actors.Add("A", aActor);

            var root = new Actor(session, Const.SELF, null);
            root.On(Const.RUN, aActor);
            root.On(Const.ERR, new Actor(session, "E", null));
            root.On(Const.TRC, new Actor(session, "T", null));
            actors.Add(Const.SELF, root);


            var folder = GetTempFolder();
            var vis = new Visualizer(actors);
            vis.Run(folder, "dotnet-name");
            var fileName = Path.Combine(folder, "dotnet-name.png");

            Assert.True(File.Exists(fileName));
        }


    }
}