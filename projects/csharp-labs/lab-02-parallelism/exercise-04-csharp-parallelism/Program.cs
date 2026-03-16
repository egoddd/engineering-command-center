using System;
using System.Diagnostics;
using System.Threading.Tasks;

class Program
{
    static void Main()
    {
        const long N = 2_000_000_000; 

        var sw = Stopwatch.StartNew();
        Countdown(N);
        Countdown(N);
        sw.Stop();
        Console.WriteLine($"Single-threaded: {sw.Elapsed.TotalSeconds:F4}s");

        sw.Restart();
        var t1 = Task.Run(() => Countdown(N));
        var t2 = Task.Run(() => Countdown(N));
        Task.WaitAll(t1, t2);
        sw.Stop();
        Console.WriteLine($"Two tasks: {sw.Elapsed.TotalSeconds:F4}s");
    }

    static void Countdown(long n)
    {
        while (n > 0)
        {
            n--;
        }
    }
}