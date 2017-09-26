using System;
using E2c;

namespace Quickstart2
{
    class Program
    {   
        public class MyAction 
        {
            public void Invoke(string data, Output<string> render, Output<string> log)
            {
                render.Invoke(data);
                log.Invoke("render done");
            } 
        }

        static void Main(string[] args)
        {
            var config = new string[] {           
               ".run -- action",
               "    action.render -- render",
               "        render.output -- .out",
               "    action.log -- log",
               "        log.store -- .out"
            };

            var session = new Session(config);
            session.Actor("action", new MyAction(), "Invoke");
            session.Actor("render", new Action<string, Output<string>>(
                (data, output) => output.Invoke(data) ));
            session.Actor("log", new Action<string, Output<string>>(
                (data, store) => store.Invoke(data) ));
            
            session.RunContinues<string, string>(
                "Hello, E2C", Console.WriteLine);
            session.Visualize();
        }
    }
}
