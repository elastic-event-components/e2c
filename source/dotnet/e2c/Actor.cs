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
using System.Reflection;

namespace E2c
{
    /// <summary>
    /// A wrapper around a callable function.
    /// </summary>
    public class Actor
    {
        private BaseSession session;
        public string Name;
        public object callable;
        public Dictionary<string, List<Actor>> Actors;
        private Dictionary<string, Type> specs;
        private MethodInfo methodInfo;

        /// <summary>
        /// A wrapper around a callable function.
        /// </summary>
        /// <param name="session">The session to that the actor belong.</param>
        /// <param name="name">The name of the actor to register on the session.</param>
        /// <param name="callable">Any callable method.</param>
        public Actor(BaseSession session, string name, object callable)
        {
            this.session = session;
            this.Name = name;
            this.Actors = new Dictionary<string, List<Actor>>();
            this.specs = new Dictionary<string, Type>();
            this.methodInfo = null;
            this.callable = callable;
        }

        /// <summary>
        ///  Method to register the given actor under specified name.
        /// </summary>
        /// <param name="name">The name to register the actor in this actor.</param>
        /// <param name="actor">An instance of the actor to register.</param>
        public void On(string name, Actor actor)
        {
            if (string.IsNullOrEmpty(name))
                throw new E2CActorError("Name cannot be null or empty!");
            if (!this.Actors.ContainsKey(name))
                this.Actors.Add(name, new List<Actor>());
            this.Actors[name].Add(actor);
        }

        /// <summary>
        /// Run the callable method with specified arguments.
        /// </summary>
        /// <param name="arguments">A list of arguments.</param>
        /// <returns>The result of the callable function.</returns>
        private object Call(object[] arguments)
        {
            var action = (Delegate)this.callable;
            try
            {
                return action.Method.Invoke(action.Target, arguments);
            }
            catch (TargetInvocationException exc)
            {
                throw exc.InnerException ?? exc;
            }
        }

        /// <summary>
        /// Run the callable internal method with secified arguments.
        /// </summary>
        /// <param name="arguments">A list of arguments.</param>
        /// <returns>The result of the callable method.</returns>
        public object Run(params object[] arguments)
        {
            var parameters = Resolver.Resolve(this, arguments);
            if (this.session.activateTrace)
                this.session.OnTrace(this.Name);
            if (this.callable == null)
                throw new E2CActorError(
                    String.Format(
                        "Actor {0} has no callable function!", this.Name));
            return this.Call(parameters);
        }

        /// <summary>
        /// Run the callable internal method with specified parameters.
        /// </summary>
        /// <param name="parameters">A list of parameters.</param>
        /// <returns>The result of the callable function.</returns>
        public object RunWithParams(params object[] parameters)
        {
            if (this.session.activateTrace)
                this.session.OnTrace(this.Name);
            return this.Call(parameters);
        }

        /// <summary>
        /// Get a new instance of that actor.
        /// </summary>
        /// <returns>The flat clone of that actor.</returns>
        public Actor Clone()
        {
            var actor = new Actor(this.session, this.Name, this.callable);
            // actor.SetCallable(this.callable);
            foreach (var item in this.Actors)
                foreach (Actor n in item.Value)
                    actor.On(item.Key, n);
            return actor;
        }

        /// <summary>
        /// Getter property to get the introspection parameter 
        /// of the internal callable function.
        /// </summary>
        /// <returns>A dictionary of name and type for each parameter.</returns>
        private MethodInfo MethodInfo
        {
            get
            {
                if (this.methodInfo == null)
                {
                    var method = (Delegate)this.callable;
                    this.methodInfo = method.GetMethodInfo();
                }
                return this.methodInfo;
            }
        }

        /// <summary>
        /// Getter property to get the introspection parameter
        /// of the internal callable function.
        /// </summary>
        /// <returns> A dictionary of name and type for each parameter.</returns>
        public Dictionary<string, Type> Specs
        {
            get
            {
                if (this.specs.Count == 0 && this.callable != null)
                {
                    foreach (var info in this.MethodInfo.GetParameters())
                        this.specs.Add(info.Name, info.ParameterType);
                }
                return this.specs;
            }
        }

    }
}