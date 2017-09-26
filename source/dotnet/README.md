<div align="center">
  <img src="https://github.com/elastic-event-components/e2c/blob/master/images/e2c-logo.png"><br><br>
</div>

# E2C.net - Elastic Event Components for .NET

**Elastic Event Components** is an open source software library to build flexible component using
function flow graphs. The graph nodes represent any operations, while
the graph edges represent the function parameters that build
the flow between nodes. Elastic Event Components also includes flow visualization.

## Installation
*See [Installing E2C](https://github.com/elastic-event-components/e2c/blob/master/INSTALL.md) for instructions 
on how to build from source.*

#### *Try your first E2C program*

```dotnet
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
            
            session.Visualize();
            session.RunContinues<string, string>(
                "Hello, E2C", Console.WriteLine);
        }
    }
}

Hello, E2C
Render done!
```

<div align="center">
  <img src="https://github.com/elastic-event-components/e2c/blob/master/images/quickstart.png"><br><br>
</div>


## For more information
* [E2C website](http://www.elastic-event-components.org)

## License
[Apache 2.0 License](LICENSE)
