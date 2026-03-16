using System;
using System.Diagnostics;

internal class Program
{
    private static void Main()
    {
        var stopwatch = Stopwatch.StartNew();

        long result = SumToN(10_000_000);

        stopwatch.Stop();

        Console.WriteLine($"Result: {result}");
        Console.WriteLine($"Elapsed time: {stopwatch.Elapsed.TotalSeconds:F6} seconds");
    }

    private static long SumToN(int n)
    {
        long total = 0;

        for (int i = 1; i <= n; i++)
        {
            total += i;
        }

        return total;
    }
}