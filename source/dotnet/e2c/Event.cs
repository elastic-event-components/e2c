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

using System.Collections.Generic;

namespace E2c
{
    /// <summary>
    /// A wrapper around the callable action.
    /// </summary>
    public class Event
    {
        internal Actor actor = null;
        private IList<Actor> continues = null;

        /// <summary>
        /// A wrapper around the callable action.
        /// </summary>
        /// <param name="actor">The actor.</param>
        /// <param name="continues">The related actors.</param>
        public Event(Actor actor, IList<Actor> continues)
        {
            this.actor = actor;
            this.continues = continues ?? new List<Actor>();
        }

        /// <summary>
        /// The method to invoke the callable wrapped action.
        /// </summary>
        /// <param name="arguments">The arguments to hand over.</param>
        /// <returns></returns>
        protected object InternalInvoke(params object[] arguments)
        {
            object[] parameters = Resolver.Resolve(this.actor, arguments);
            object result = this.actor.RunWithParams(parameters);
            foreach (Actor continuesActor in this.continues)
                continuesActor.Run(arguments);
            return result;
        }
    }

    public class Input<TResult> : Event
    {
        public Input(Actor actor, IList<Actor> continues) : base(actor, continues) { }

        public TResult Invoke()
        {
            return (TResult)this.InternalInvoke(new object[] { });
        }
    }

    public class Input<T1, TResult> : Event
    {
        public Input(Actor actor, IList<Actor> continues) : base(actor, continues) { }

        public TResult Invoke(T1 arg1)
        {
            return (TResult)this.InternalInvoke(new object[] { arg1 });
        }
    }

    public class Input<T1, T2, TResult> : Event
    {
        public Input(Actor actor, IList<Actor> continues) : base(actor, continues) { }

        public TResult Invoke(T1 arg1, T2 arg2)
        {
            return (TResult)this.InternalInvoke(new object[] { arg1, arg2 });
        }
    }

    public class Input<T1, T2, T3, TResult> : Event
    {
        public Input(Actor actor, IList<Actor> continues) : base(actor, continues) { }

        public TResult Invoke(T1 arg1, T2 arg2, T3 arg3)
        {
            return (TResult)this.InternalInvoke(new object[] { arg1, arg2, arg3 });
        }
    }

    public class Input<T1, T2, T3, T4, TResult> : Event
    {
        public Input(Actor actor, IList<Actor> continues) : base(actor, continues) { }

        public TResult Invoke(T1 arg1, T2 arg2, T3 arg3, T4 arg4)
        {
            return (TResult)this.InternalInvoke(new object[] { arg1, arg2, arg3, arg4 });
        }
    }

    public class Input<T1, T2, T3, T4, T5, TResult> : Event
    {
        public Input(Actor actor, IList<Actor> continues) : base(actor, continues) { }

        public TResult Invoke(T1 arg1, T2 arg2, T3 arg3, T4 arg4, T5 arg5)
        {
            return (TResult)this.InternalInvoke(new object[] { arg1, arg2, arg3, arg4, arg5 });
        }
    }

    public class Input<T1, T2, T3, T4, T5, T6, TResult> : Event
    {
        public Input(Actor actor, IList<Actor> continues) : base(actor, continues) { }

        public TResult Invoke(T1 arg1, T2 arg2, T3 arg3, T4 arg4, T5 arg5, T6 arg6)
        {
            return (TResult)this.InternalInvoke(new object[] { arg1, arg2, arg3, arg4, arg5, arg6 });
        }
    }

    public class Input<T1, T2, T3, T4, T5, T6, T7, TResult> : Event
    {
        public Input(Actor actor, IList<Actor> continues) : base(actor, continues) { }

        public TResult Invoke(T1 arg1, T2 arg2, T3 arg3, T4 arg4, T5 arg5, T6 arg6, T7 arg7)
        {
            return (TResult)this.InternalInvoke(new object[] { arg1, arg2, arg3, arg4, arg5, arg6, arg7 });
        }
    }

    public class Input<T1, T2, T3, T4, T5, T6, T7, T8, TResult> : Event
    {
        public Input(Actor actor, IList<Actor> continues) : base(actor, continues) { }

        public TResult Invoke(T1 arg1, T2 arg2, T3 arg3, T4 arg4, T5 arg5, T6 arg6, T7 arg7, T8 arg8)
        {
            return (TResult)this.InternalInvoke(new object[] { arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8 });
        }
    }

    public class Input<T1, T2, T3, T4, T5, T6, T7, T8, T9, TResult> : Event
    {
        public Input(Actor actor, IList<Actor> continues) : base(actor, continues) { }

        public TResult Invoke(T1 arg1, T2 arg2, T3 arg3, T4 arg4, T5 arg5, T6 arg6, T7 arg7, T8 arg8, T9 arg9)
        {
            return (TResult)this.InternalInvoke(new object[] { arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9 });
        }
    }

    public class Input<T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, TResult> : Event
    {
        public Input(Actor actor, IList<Actor> continues) : base(actor, continues) { }

        public TResult Invoke(T1 arg1, T2 arg2, T3 arg3, T4 arg4, T5 arg5, T6 arg6, T7 arg7, T8 arg8, T9 arg9, T10 arg10)
        {
            return (TResult)this.InternalInvoke(new object[] { arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10 });
        }
    }

    public class Input<T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11, TResult> : Event
    {
        public Input(Actor actor, IList<Actor> continues) : base(actor, continues) { }

        public TResult Invoke(T1 arg1, T2 arg2, T3 arg3, T4 arg4, T5 arg5, T6 arg6, T7 arg7, T8 arg8, T9 arg9, T10 arg10, T11 arg11)
        {
            return (TResult)this.InternalInvoke(new object[] { arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11 });
        }
    }

    public class Input<T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11, T12, TResult> : Event
    {
        public Input(Actor actor, IList<Actor> continues) : base(actor, continues) { }

        public TResult Invoke(T1 arg1, T2 arg2, T3 arg3, T4 arg4, T5 arg5, T6 arg6, T7 arg7, T8 arg8, T9 arg9, T10 arg10, T11 arg11, T12 arg12)
        {
            return (TResult)this.InternalInvoke(new object[] { arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12 });
        }
    }

    public class Output : Event
    {
        public Output(Actor actor, IList<Actor> continues) : base(actor, continues) { }

        public void Invoke()
        {
            this.InternalInvoke(new object[] { });
        }
    }

    public class Output<T1> : Output
    {
        public Output(Actor actor, IList<Actor> continues) : base(actor, continues) { }

        public void Invoke(T1 arg1)
        {
            this.InternalInvoke(new object[] { arg1 });
        }
    }

    public class Output<T1, T2> : Output
    {
        public Output(Actor actor, IList<Actor> continues) : base(actor, continues) { }

        public void Invoke(T1 arg1, T2 arg2)
        {
            this.InternalInvoke(new object[] { arg1, arg2 });
        }
    }

    public class Output<T1, T2, T3> : Output
    {
        public Output(Actor actor, IList<Actor> continues) : base(actor, continues) { }

        public void Invoke(T1 arg1, T2 arg2, T3 arg3)
        {
            this.InternalInvoke(new object[] { arg1, arg2, arg3 });
        }
    }

    public class Output<T1, T2, T3, T4> : Output
    {
        public Output(Actor actor, IList<Actor> continues) : base(actor, continues) { }

        public void Invoke(T1 arg1, T2 arg2, T3 arg3, T4 arg4)
        {
            this.InternalInvoke(new object[] { arg1, arg2, arg3, arg4 });
        }
    }

    public class Output<T1, T2, T3, T4, T5> : Output
    {
        public Output(Actor actor, IList<Actor> continues) : base(actor, continues) { }

        public void Invoke(T1 arg1, T2 arg2, T3 arg3, T4 arg4, T5 arg5)
        {
            this.InternalInvoke(new object[] { arg1, arg2, arg3, arg4, arg5 });
        }
    }

    public class Output<T1, T2, T3, T4, T5, T6> : Output
    {
        public Output(Actor actor, IList<Actor> continues) : base(actor, continues) { }

        public void Invoke(T1 arg1, T2 arg2, T3 arg3, T4 arg4, T5 arg5, T6 arg6)
        {
            this.InternalInvoke(new object[] { arg1, arg2, arg3, arg4, arg5, arg6 });
        }
    }

    public class Output<T1, T2, T3, T4, T5, T6, T7> : Output
    {
        public Output(Actor actor, IList<Actor> continues) : base(actor, continues) { }

        public void Invoke(T1 arg1, T2 arg2, T3 arg3, T4 arg4, T5 arg5, T6 arg6, T7 arg7)
        {
            this.InternalInvoke(new object[] { arg1, arg2, arg3, arg4, arg5, arg6, arg7 });
        }
    }

    public class Output<T1, T2, T3, T4, T5, T6, T7, T8> : Output
    {
        public Output(Actor actor, IList<Actor> continues) : base(actor, continues) { }

        public void Invoke(T1 arg1, T2 arg2, T3 arg3, T4 arg4, T5 arg5, T6 arg6, T7 arg7, T8 arg8)
        {
            this.InternalInvoke(new object[] { arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8 });
        }
    }

    public class Output<T1, T2, T3, T4, T5, T6, T7, T8, T9> : Output
    {
        public Output(Actor actor, IList<Actor> continues) : base(actor, continues) { }

        public void Invoke(T1 arg1, T2 arg2, T3 arg3, T4 arg4, T5 arg5, T6 arg6, T7 arg7, T8 arg8, T9 arg9)
        {
            this.InternalInvoke(new object[] { arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9 });
        }
    }

    public class Output<T1, T2, T3, T4, T5, T6, T7, T8, T9, T10> : Output
    {
        public Output(Actor actor, IList<Actor> continues) : base(actor, continues) { }

        public void Invoke(T1 arg1, T2 arg2, T3 arg3, T4 arg4, T5 arg5, T6 arg6, T7 arg7, T8 arg8, T9 arg9, T10 arg10)
        {
            this.InternalInvoke(new object[] { arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10 });
        }
    }

    public class Output<T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11> : Output
    {
        public Output(Actor actor, IList<Actor> continues) : base(actor, continues) { }

        public void Invoke(T1 arg1, T2 arg2, T3 arg3, T4 arg4, T5 arg5, T6 arg6, T7 arg7, T8 arg8, T9 arg9, T10 arg10, T11 arg11)
        {
            this.InternalInvoke(new object[] { arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11 });
        }
    }

    public class Output<T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11, T12> : Output
    {
        public Output(Actor actor, IList<Actor> continues) : base(actor, continues) { }

        public void Invoke(T1 arg1, T2 arg2, T3 arg3, T4 arg4, T5 arg5, T6 arg6, T7 arg7, T8 arg8, T9 arg9, T10 arg10, T11 arg11, T12 arg12)
        {
            this.InternalInvoke(new object[] { arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12 });
        }
    }

}