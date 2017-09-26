using System;
using E2c;

namespace Quickstart1
{
    class Program
    {   
        static void Main(string[] args)
        {
            var config = new string[] {
               ".run -- action",
               "action.output -- print",
            };

            var session = new Session(config);
            session.Actor("action", new Action<string, Output<string>>(
                (data, output) => output.Invoke(data) ));
            session.Actor("print", new Action<string>(Console.WriteLine));

            session.Visualize();
            session.Run<string, string>("Hello, E2C");
        }
    }
}
