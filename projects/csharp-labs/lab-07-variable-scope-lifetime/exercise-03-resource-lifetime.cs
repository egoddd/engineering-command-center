// Exercise 3: Resource Lifetime
using System;
using System.IO;

public class TradeFileReader : IDisposable
{
    private StreamReader _reader;
    private bool _disposed = false;

    public TradeFileReader(string path)
    {
        _reader = new StreamReader(path);
        Console.WriteLine($"Opened file: {path}");
    }

    public string ReadLine()
    {
        if (_disposed)
            throw new ObjectDisposedException(nameof(TradeFileReader));

        return _reader.ReadLine();
    }

    public void Dispose()
    {
        if (!_disposed)
        {
            _reader?.Dispose();
            _disposed = true;
            Console.WriteLine("Closed file");
        }
    }
}

class Program
{
    static void Main()
    {
        string path = "trades.txt";
        File.WriteAllText(path, "TRADE1\nTRADE2\n");

        try
        {
            using (var reader = new TradeFileReader(path))
            {
                Console.WriteLine("Inside using block");
                Console.WriteLine("Read: " + reader.ReadLine());

                throw new Exception("Something failed during processing");
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine("Caught exception: " + ex.Message);
        }

        Console.WriteLine("Program continues after exception");
    }
}