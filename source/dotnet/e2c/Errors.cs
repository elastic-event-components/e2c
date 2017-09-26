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

namespace E2c
{
    /// <summary>
    /// The error class to throw exceptions in class Analyser.
    /// </summary>
    public class E2CSessionError : Exception
    {
        public E2CSessionError()
        { }
        public E2CSessionError(string message) : base(message)
        { }
        public E2CSessionError(string message, Exception innerException)
            : base(message, innerException)
        { }
    }

    /// <summary>
    /// The error class to throw exceptions in class Actor.
    /// </summary>
    public class E2CActorError : Exception
    {
        public E2CActorError()
        { }
        public E2CActorError(string message) : base(message)
        { }
        public E2CActorError(string message, Exception innerException)
            : base(message, innerException)
        { }
    }

    /// <summary>
    /// The error class to throw exceptions in class Resolve.
    /// </summary>
    public class E2CResolveError : Exception
    {
        public E2CResolveError()
        { }
        public E2CResolveError(string message) : base(message)
        { }
        public E2CResolveError(string message, Exception innerException)
            : base(message, innerException)
        { }
    }


    /// <summary>
    /// The error class to throw exceptions in class Visualizer.
    /// </summary>
    public class E2CVisualizeError : System.Exception
    {
        public E2CVisualizeError()
        { }
        public E2CVisualizeError(string message) : base(message)
        { }
        public E2CVisualizeError(string message, Exception innerException)
            : base(message, innerException)
        { }
    }

    /// <summary>
    /// The error class to throw exceptions in class Parser.
    /// </summary>
    public class E2CParserError : System.Exception
    {
        public E2CParserError()
        { }
        public E2CParserError(string message) : base(message)
        { }
        public E2CParserError(string message, Exception innerException)
            : base(message, innerException)
        { }
    }

    /// <summary>
    /// The error class to throw exceptions in class Analyser.
    /// </summary>
    public class E2CAnalyserError : System.Exception
    {
        public E2CAnalyserError()
        { }
        public E2CAnalyserError(string message) : base(message)
        { }
        public E2CAnalyserError(string message, Exception innerException)
            : base(message, innerException)
        { }
    }

}