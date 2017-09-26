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
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Text;

namespace E2c
{
    /// <summary>
    /// The class to visualize actors and relations.
    /// </summary>
    public class Visualizer
    {
        private const string FORMAT = "png";

        private Dictionary<string, Actor> actors;

        /// <summary>
        ///  The class to visualize actors and relations.
        /// </summary>
        /// <param name="actors">The actors to analyse.</param>
        public Visualizer(Dictionary<string, Actor> actors)
        {
            this.actors = actors;
        }

        /// <summary>
        /// Starts the visualizing.
        /// </summary>
        /// <param name="folder">The folder to store the output.</param>
        /// <param name="name">The name of the graph.</param>
        public virtual void Run(string folder, string name)
        {
            var script = CreateScript(name);
            WriteGraph(folder, name, script);
        }

        /// <summary>
        /// Creates the script to builds the graph.
        /// </summary>
        /// <param name="name">The name of the diagram.</param>
        /// <returns>The script.</returns>
        private string CreateScript(string name)
        {
            var script = new StringBuilder();
            var anyActor = false;
            foreach (var actor in this.actors)
            {
                var leftActorName = actor.Key;
                var leftActor = actor.Value;
                foreach (var leftChildActor in leftActor.Actors)
                {
                    var leftParam = leftChildActor.Key;
                    var rightActors = leftChildActor.Value;
                  
                    anyActor = true;
                    if (leftActorName == Const.SELF)
                        script.Append(this.Node(leftActorName, "color=orange"));
                  
                    foreach (var relationActor in rightActors)
                    {
                        if (relationActor.Name == Const.OUT)
                            script.Append(this.Node(relationActor.Name, "color=orange"));

                        string attribute = String.Format("label={0}", leftParam);
                        if (leftParam == Const.ERR)
                            attribute += " color=red fontcolor=red";
                        if (leftParam == Const.TRC)
                            attribute += " color=darkorchid1 fontcolor=darkorchid1";

                        script.Append(this.Edge(
                            leftActor.Name, relationActor.Name, attribute));
                    }

                }
            }

            if (!anyActor)
                throw new E2CVisualizeError("Graph is empty!");

            var template = GetTemplate();
            template = template.Replace("[x1]", name);
            return template.Replace("[x2]", script.ToString());
        }

        /// <summary>
        /// Returns a parameterized node.
        /// </summary>
        /// <param name="name">The name of the node.</param>
        /// <param name="attribute">The attibutes like color.</param>
        /// <returns>A string that represents the node.</returns>
        private string Node(string name, string attribute)
        {
            return String.Format("\"{0}\"[{1}]\n ", name, attribute);
        }

        /// <summary>
        /// Returns a parameterized edge.
        /// </summary>
        /// <param name="node1">The name of the first node.</param>
        /// <param name="node2">The name of the second node.</param>
        /// <param name="attribute">The attributes like color.</param>
        /// <returns>A string that represents the edge.</returns>
        private string Edge(string node1, string node2, string attribute)
        {
            return String.Format("\"{0}\" -> \"{1}\"[{2}]\n ", node1, node2, attribute);
        }

        /// <summary>
        /// Gets the template string of the graph.
        /// This is the head of the diagram.
        /// </summary>
        /// <returns></returns>
        private string GetTemplate()
        {
            return @"
                digraph {
	                graph [label=""[x1]"" labeljust=r]
	                node [color=black fontcolor=black]
	                edge [color=orange fontcolor=orange]
                    [x2]
                }";
        }

        /// <summary>
        /// Writes the source to given folder.
        /// </summary>
        /// <param name="folder">The folder to write.</param>
        /// <param name="name">The name of the file.</param>
        /// <param name="graphSource">The source to build the diagram.</param>
        private void WriteGraph(string folder, string name, string graphSource)
        {
            if (!String.IsNullOrEmpty(folder))
                folder = Directory.CreateDirectory(folder).FullName;
            else
                folder = Directory.GetCurrentDirectory();
            var filename = String.Format(
                  "{0}{1}{2}.{3}", folder, Path.DirectorySeparatorChar, name, FORMAT);

            var processInfo = new ProcessStartInfo(
                "dot", String.Format("-T{0} -o {1}", FORMAT, filename));

            processInfo.CreateNoWindow = true;
            processInfo.WindowStyle = ProcessWindowStyle.Hidden;
            processInfo.UseShellExecute = false;
            processInfo.RedirectStandardInput = true;

            var app = new Process { StartInfo = processInfo };
            app.Start();
            try
            {
                app.StandardInput.Write(graphSource);
                app.StandardInput.Flush();
            }
            finally
            {
                app.StandardInput.Close();
            }
            app.WaitForExit();
        }
    }
}