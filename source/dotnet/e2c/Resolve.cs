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
    /// The helper class to find missing parameters.
    /// </summary>
    public class Resolver
    {
        /// <summary>
        /// The method to find missing parameters in specified actor.
        /// </summary>
        /// <param name="actor">The actor, at which the parameters are verified</param>
        /// <param name="values">A list of values to add to the parameters on the first position.</param>
        /// <returns>A list of parameters to run the actor.</returns>
        public static object[] Resolve(Actor actor, object[] values)
        {
            var parameters = new List<object>();
            var valueList = new List<object>(values);
            foreach (var item in actor.Specs)
            {
                Actor inputActor = null;
                List<Actor> actors = new List<Actor>();
                if (actor.Actors.ContainsKey(item.Key))
                {
                    actors = actor.Actors[item.Key];
                    inputActor = actors[0];
                }

                if (inputActor == null && valueList.Count > 0)
                {
                    parameters.Add(valueList[0]);
                    valueList.RemoveAt(0);
                }
                else if (inputActor != null)
                {
                    // ignore first param.
                    if (!item.Value.IsSubclassOf(typeof(Event)))
                        throw new E2CResolveError(
                            String.Format("Cannot resolve type {0}", item.Value));

                    var callable = Activator.CreateInstance(
                        item.Value, inputActor, actors.GetRange(1, actors.Count - 1));
                    parameters.Add(callable);
                }
                else
                {
                    parameters.Add(null);
                }
            }
            return parameters.ToArray();
        }
    }

}