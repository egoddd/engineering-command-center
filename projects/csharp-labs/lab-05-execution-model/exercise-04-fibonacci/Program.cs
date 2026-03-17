using System;
using System.Diagnostics;

class Program
{
    static int FibRecursive(int n)
    {
        if (n <= 1)
            return n;

        return FibRecursive(n - 1) + FibRecursive(n - 2);
    }

    static int FibIterative(int n)
    {
        int a = 0, b = 1;

        for (int i = 2; i <= n; i++)
        {
            int temp = a + b;
            a = b;
            b = temp;
        }

        return b;
    }

    static void Main()
    {
        const int N = 40;
        const int repetitions = 10000;

        var sw = Stopwatch.StartNew();

        for (int i = 0; i < repetitions; i++)
            FibRecursive(N);

        sw.Stop();
        Console.WriteLine($"Recursive: {sw.Elapsed}");

        sw.Restart();

        for (int i = 0; i < repetitions; i++)
            FibIterative(N);

        sw.Stop();
        Console.WriteLine($"Iterative: {sw.Elapsed}");
    }
}