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
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq.Expressions;
using System.Reflection;

namespace E2c
{
    /// <summary>
    /// The class to represents the result.
    /// </summary>
    public class Result
    {
        public object Value;
        public Action<object> ValueCallback;

        /// <summary>
        /// The class to represents the result.
        /// </summary>
        public Result()
        {
            this.Value = null;
            this.ValueCallback = null;
        }

        /// <summary>
        /// The method to set the value.
        /// </summary>
        /// <param name="data">Any data.</param>
        public void set(object data)
        {
            if (this.ValueCallback != null)
            {
                this.ValueCallback(data);
            }
            else
            {
                this.Value = data;
            }
        }
    }

    /// <summary>
    /// The core session brings all components together.
    /// </summary>
    public class BaseSession
    {
        private Result result = null;
        private Output<object> tracer = null;
        private Output<object> end = null;
        public string Name = string.Empty;
        private Analyser analyser = null;
        private Parser parser = null;
        private Visualizer visualizer = null;
        private Dictionary<string, Actor> actors = null;
        internal bool activateTrace = true;

        /// <summary>
        /// Inits the session and brings all players together.
        /// </summary>
        /// <param name="actors">The actors to work with.</param>
        /// <param name="analyser">A instance of the analyser.</param>
        /// <param name="parser">A instance of the parser.</param>
        /// <param name="visualizer">A instance of the visualiser.</param>
        /// <param name="script">The string list of the graph to parse.</param>
        protected void Init(
            Dictionary<string, Actor> actors, Analyser analyser,
            Parser parser, Visualizer visualizer, string[] script)
        {
            this.Name = Const.DEFAULT;
            this.analyser = analyser;
            this.parser = parser;
            this.visualizer = visualizer;
            this.result = new Result();
            this.tracer = null;
            this.end = null;
            this.actors = actors;
            this.Actor<Action<string, Output<object>, Output<object>, Output<object>, Output<object>>>(Const.SELF, this.process); // TODO: missing function.
            this.Actor<Action<object>>(Const.OUT, this.result.set);
            if (script != null)
                this.ParseGraph(script);
        }

        /// <summary>
        ///  The method to start the first actor after call 'run'.
        /// </summary>
        /// <param name="request">The data to be transmitted.</param>
        /// <param name="run">The run function.</param>
        /// <param name="end">The end function.</param>
        /// <param name="err">The error function.</param>
        /// <param name="trace">The trace function.</param>
        public void process(object request, Output<object> run, Output<object> end, Output<object> err, Output<object> trace)
        {
            try
            {
                this.tracer = trace;
                this.end = end;
                if (run == null)
                    throw new E2CSessionError(String.Format(
                        "Missing .{0} -- ? in graph!", Const.RUN));
                run.Invoke(request);
            }
            catch (Exception exc)
            {
                if (err == null)
                    throw exc;
                err.Invoke(exc);
            }
        }

        /// <summary>
        /// The method to track the trace path.
        /// </summary>
        /// <param name="name">The name of the running actor.</param>
        public void OnTrace(string name)
        {
            if (this.tracer != null)
            {
                try
                {
                    // deactivate trace in tracing process
                    // to avoid recursion
                    this.activateTrace = false;
                    if (name != Const.OUT)
                        this.tracer.Invoke(name);
                }
                finally
                {
                    this.activateTrace = true;
                }
            }
        }

        /// <summary>
        /// Register a new actor by specified name and the callable method.
        /// </summary>
        /// <param name="name">The name under which the function can be called.</param>
        /// <param name="action">The callable instance of the action.</param>
        private void AddActor(string name, object action)
        {
            if (this.actors.ContainsKey(name) && this.actors[name].callable != null)
                throw new E2CSessionError(
                    string.Format("Actor {0} was already registered!", name));
            if (!this.actors.ContainsKey(name))
                this.actors[name] = new Actor(this, name, null);
            this.actors[name].callable = action;
        }

        /// <summary>
        /// Register a new actor by specified name and the callable method.
        /// </summary>
        /// <param name="name">The name under which the function can be called.</param>
        /// <param name="action">The callable instance of the action.</param>
        public void Actor<T>(string name, T action)
        {
            this.AddActor(name, action);
        }

        /// <summary>
        /// Registers a new actor by specified name and the callable method.
        /// </summary>
        /// <param name="name">The name under which the function can be called.</param>
        /// <param name="instance">The instance of the class to which the specified method belongs.</param>
        /// <param name="methodName">The name of the method under which the method is registered.</param>
        /// <param name="parameterTypes">The types of the parameters of specified method.</param>
        public void Actor(string name, object instance, string methodName, Type[] parameterTypes = null)
        {
            MethodInfo method = null;
            if (parameterTypes == null)
                method = instance.GetType().GetMethod(methodName);
            else method = instance.GetType().GetMethod(methodName, parameterTypes);

            var methodArguments = new List<Type>();
            foreach (var param in method.GetParameters())
                methodArguments.Add(param.ParameterType);

            var actionType = Expression.GetActionType(methodArguments.ToArray());
            var constructor = actionType.GetConstructors()[0];
            var action = constructor.Invoke(new object[] {
                instance,
                method.MethodHandle.GetFunctionPointer()
            });

            this.AddActor(name, action);
        }

        /// <summary>
        /// Starts the analyser.
        /// </summary>
        /// <param name="quite">False to print outputs on the command line.</param>
        public void Analyse(bool quite = true)
        {
            this.analyser.Run(quite);
        }

        /// <summary>
        /// Starts the visualiser.
        /// </summary>
        /// <param name="folder">The directory where the graph is written.</param>
        public void Visualize(string folder = "")
        {
            this.visualizer.Run(folder, this.Name);
        }

        /// <summary>
        /// Opens the specified file and builds up the graph.
        /// </summary>
        /// <param name="filename">The filename to load from file.</param>
        public void LoadGraph(string filename)
        {
            try
            {
                string[] lines = File.ReadAllLines(filename);
                this.ParseGraph(lines);
            }
            catch (Exception exc)
            {
                throw new E2CSessionError(exc.Message, exc);
            }
        }

        /// <summary>
        /// Parses the script and builds the graph.
        /// </summary>
        /// <param name="script">The script to parse.</param>
        public void ParseGraph(string[] script)
        {
            this.parser.Run(script, name => this.Name = (string)name);
        }

        /// <summary>
        /// Runs the graph and returns the return value.
        /// </summary>
        /// <param name="request">The data to be transmitted.</param>
        /// <param name="actor">The optional name of the actor to start.</param>
        /// <returns>The return value.</returns>
        public TResult Run<T, TResult>(T request = default(T), string actor = null)
        {
            this.Analyse(true);
            if (String.IsNullOrEmpty(actor))
            {
                this.actors[Const.SELF].Run(request);
            }
            else
            {
                if (!this.actors.ContainsKey(actor))
                    throw new E2CSessionError(
                        String.Format("{0} is not a registered actor!", actor));

                Actor runner = this.actors[Const.SELF].Clone();
                runner.Actors[Const.RUN].Clear();
                runner.On(Const.RUN, this.actors[actor]);
                runner.Run(request);
            }
            if (this.end != null)
                this.end.actor.Run(request);
            return (TResult)this.result.Value;
        }

        /// <summary>
        ///  Runs the graph and calls a result callback.
        /// </summary>
        /// <param name="request">The data to be transmitted.</param>
        /// <param name="result">The result callback.</param>
        /// <param name="actor">The optional name of the actor to start.</param>
        /// <returns></returns>
        public void RunContinues<T, TResult>(T request, Action<TResult> result = null, string actor = null)
        {
            this.result.ValueCallback =
                new Action<object>((value) => { result.Invoke((TResult)value); });
            this.Run<T, TResult>(request, actor);
        }
    }

    /// <summary>
    ///  A class for running E2C operations.
    ///  A `Session` object encapsulates the environment in which `Actor` 
    /// objects are executed.
    /// </summary>
    public class Session : BaseSession
    {
        /// <summary>
        /// A class for running E2C operations.
        /// </summary>
        /// <param name="script">The script to builds the graph.</param>
        public Session(string[] script = null)
        {
            var actors = new Dictionary<string, Actor>();
            var analyser = new Analyser(actors);
            var parser = new Parser(actors, (string name) => new Actor(this, name, null));
            var visualizer = new Visualizer(actors);
            this.Init(actors, analyser, parser, visualizer, script);
        }

    }

}