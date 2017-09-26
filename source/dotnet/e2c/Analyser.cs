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
    /// The class to analyse actors and relations.
    /// </summary>
    public class Analyser
    {
        private Dictionary<string, Actor> actors;

        /// <summary>
        /// The class to analyse actors and relations.
        /// </summary>
        /// <param name="actors">The actors to analyse.</param>
        public Analyser(Dictionary<string, Actor> actors)
        {
            this.actors = actors ?? new Dictionary<string, Actor>();
        }

        /// <summary>
        /// Returns true when the given type is an action.
        /// </summary>
        /// <param name="type">The type to verify.</param>
        /// <returns></returns>
        static bool IsAction(Type type)
        {
            if (type == typeof(System.Action)) return true;
            Type generic = null;
            if (type.IsGenericTypeDefinition) generic = type;
            else if (type.IsGenericType) generic = type.GetGenericTypeDefinition();
            if (generic == null) return false;
            if (generic.BaseType == typeof(System.MulticastDelegate)) return true;
            return false;
        }

        /// <summary>
        /// Starts the analysing.
        /// </summary>
        /// <param name="quite">False to print outputs on the command line.</param>
        public virtual void Run(bool quite = true)
        {
            foreach (var actor in this.actors)
            {
                var actorName = actor.Key;
                var actorInstance = actor.Value;

                if (!quite)
                    Console.WriteLine("\t{0}", actorName);

                if (actorInstance.callable == null)
                    throw new E2CAnalyserError(
                        String.Format("Actor {0} has no callable function!", actorName));

                if (actorInstance.callable == null)
                    throw new E2CAnalyserError(
                        String.Format("Actor {0} has no callable function!", actorName));

                if (!IsAction(actorInstance.callable.GetType()))
                    throw new E2CAnalyserError(
                        String.Format("Actor {0} is not a callable function!", actorName));

                foreach (var childInstance in actorInstance.Actors)
                {
                    var parameterName = childInstance.Key;
                    var actors = childInstance.Value;
                    foreach (var inputActor in actors)
                    {
                        if (!quite)
                            Console.WriteLine("\t\t({0}, {1})", parameterName, inputActor.Name);
                        if (!actorInstance.Specs.ContainsKey(parameterName))
                            throw new E2CAnalyserError(
                                String.Format("{0} on actor {1} is not a parameter in the callable function!",
                                parameterName, actorName));
                    }
                }
            }
        }

    }
}