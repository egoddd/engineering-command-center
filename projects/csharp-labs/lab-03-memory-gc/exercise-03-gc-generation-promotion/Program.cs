using System;

class Demo
{
    public byte[] Data = new byte[1024];
}

class Program
{
    static void Main()
    {
        var obj = new Demo();

        Console.WriteLine($"Initial generation: {GC.GetGeneration(obj)}");

        GC.Collect(0);
        GC.WaitForPendingFinalizers();
        GC.Collect(0);
        Console.WriteLine($"After Gen 0 collect: {GC.GetGeneration(obj)}");

        GC.Collect(1);
        GC.WaitForPendingFinalizers();
        GC.Collect(1);
        Console.WriteLine($"After Gen 1 collect: {GC.GetGeneration(obj)}");

        GC.Collect(2);
        GC.WaitForPendingFinalizers();
        GC.Collect(2);
        Console.WriteLine($"After Gen 2 collect: {GC.GetGeneration(obj)}");
    }
}