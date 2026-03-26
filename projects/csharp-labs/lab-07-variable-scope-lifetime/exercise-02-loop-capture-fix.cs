// Exercise 2: Loop Capture Fix (C#)
using System;
using System.Collections.Generic;

class Program
{
    static void Main()
    {
        Console.WriteLine("Broken loop capture:");
        var funcs = new List<Func<int>>();

        for (int i = 0; i < 3; i++)
        {
            funcs.Add(() => i); // captures the same loop variable
        }

        foreach (var f in funcs)
        {
            Console.WriteLine(f()); // likely prints 3, 3, 3
        }

        Console.WriteLine("\nFixed loop capture:");
        var fixedFuncs = new List<Func<int>>();

        for (int i = 0; i < 3; i++)
        {
            int copy = i; // capture a separate variable each iteration
            fixedFuncs.Add(() => copy);
        }

        foreach (var f in fixedFuncs)
        {
            Console.WriteLine(f()); // prints 0, 1, 2
        }
    }
}