using System;
using System.Diagnostics;
using System.Threading;
using System.Threading.Tasks;

internal class Program
{
    private static async Task Main()
    {
        Console.WriteLine("=== C# Program Execution Demo ===");
        Console.WriteLine($"Process ID: {Process.GetCurrentProcess().Id}");
        Console.WriteLine($"Main Thread ID: {Environment.CurrentManagedThreadId}");

        int value = 42;
        int[] numbers = { 1, 2, 3, 4, 5 };

        Console.WriteLine($"Value on execution path: {value}");
        Console.WriteLine($"Array object in memory: [{string.Join(", ", numbers)}]");

        await Task.Run(() =>
        {
            Console.WriteLine($"[Worker] Thread ID: {Environment.CurrentManagedThreadId}");
            Thread.Sleep(1000);
            Console.WriteLine("[Worker] Finished work.");
        });

        Console.WriteLine("Program finished.");
    }
}