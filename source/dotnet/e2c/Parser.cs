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

namespace E2c
{
    /// <summary>
    /// Represents a class to parse the graph and build relations between them.
    /// </summary>
    public class Parser
    {
        private Dictionary<string, Actor> actors;
        private Func<string, Actor> createActor;

        /// <summary>
        /// Represents a class to parse the graph and build relations between them.
        /// </summary>
        /// <param name="actors">The list to add the handeled actors.</param>
        /// <param name="createActor">The function to build new actors.</param>
        public Parser(Dictionary<string, Actor> actors, Func<string, Actor> createActor)
        {
            this.actors = actors;
            this.createActor = createActor;
        }

        /// <summary>
        /// Starts the parsing.
        /// </summary>
        /// <param name="script">The script to parse.</param>
        /// <param name="outName">The function to receive the name of graph.</param>
        public void Run(string[] script, Func<object, string> outName)
        {           
            if (String.Join("", script).Trim() == String.Empty)
                throw new E2CParserError("No data to parse!");

            int index = 0;
            foreach (string nextLine in script)
            {
                index++;
                string line = nextLine.Replace(
                    "\n", String.Empty).Replace(
                        " ", String.Empty).Trim();

                if (string.IsNullOrEmpty(line))
                    continue;

                int pos = line.IndexOf(Const.COMMENT);
                if (pos >= 0)
                {
                    line = line.Substring(0, pos);
                    if (String.IsNullOrEmpty(line))
                        continue;
                }

                if (line.StartsWith("[") && line.EndsWith("]"))
                {
                    outName(line.Substring(1, line.Length - 2));
                    continue;
                }

                if (!line.Contains(Const.EDGE))
                    throw new E2CParserError(
                        String.Format(
                            "Missing {0} in line {1}!", Const.EDGE, index));

                var (leftActorNameAndParam, rightActorName) = this.Split(line, Const.EDGE);
                if (String.IsNullOrEmpty(rightActorName))
                    throw new E2CParserError(
                        String.Format(
                            "Missing actor in line {0}!", index));

                var (leftActorName, leftParam) = this.Split(leftActorNameAndParam, ".");
                if (String.IsNullOrEmpty(leftActorName))
                    leftActorName = Const.SELF;

                if (!this.actors.ContainsKey(leftActorName))
                    this.actors.Add(leftActorName, this.createActor(leftActorName));
                if (!this.actors.ContainsKey(rightActorName))
                    this.actors.Add(rightActorName, this.createActor(rightActorName));

                this.actors[leftActorName].On(
                    leftParam, this.actors[rightActorName]);
            }

        }

        /// <summary>
        /// Represents the helper method to split the specified 
        /// line by given seperator.
        /// </summary>
        /// <param name="line"></param>
        /// <param name="seperator"></param>
        /// <returns></returns>
        private Tuple<string, string> Split(string line, string seperator)
        {
            string[] result = line.Split(new String[]{seperator}, StringSplitOptions.None);
            return new Tuple<string, string>(result[0], result[1]);
        }

    }
}