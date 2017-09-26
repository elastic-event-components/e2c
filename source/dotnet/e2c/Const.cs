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

namespace E2c
{
    /// <summary>
    /// Represents the class to contains the constants.
    /// </summary>
    public class Const {

        public static string SELF = "•";
        public static string EDGE = "--";
        public static string COMMENT = "//";
        public static string DEFAULT = "default";

        // operations - on left side of '--'
        public static string RUN = "run";
        public static string ERR = "err";
        public static string TRC = "trace";

        // events - on right side of '--'
        public static string OUT = ".out";
    }
}