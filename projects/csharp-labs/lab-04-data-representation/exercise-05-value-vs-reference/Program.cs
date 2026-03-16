using System;

struct Position
{
    public int Quantity;
}

class Portfolio
{
    public int Quantity;
}

class Program
{
    static void IncreasePosition(Position p)
    {
        p.Quantity += 10;
    }

    static void IncreasePortfolio(Portfolio p)
    {
        p.Quantity += 10;
    }

    static void IncreasePositionCorrect(ref Position p)
    {
        p.Quantity += 10;
    }

    static void Main()
    {
        var pos = new Position { Quantity = 100 };
        IncreasePosition(pos);
        Console.WriteLine($"Position after buggy call: {pos.Quantity}");

        IncreasePositionCorrect(ref pos);
        Console.WriteLine($"Position after correct call: {pos.Quantity}");

        var portfolio = new Portfolio { Quantity = 100 };
        IncreasePortfolio(portfolio);
        Console.WriteLine($"Portfolio after call: {portfolio.Quantity}");
    }
}