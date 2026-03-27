using System;
using System.Collections.Generic;
using System.Linq;

public class Trade
{
    public string Symbol { get; set; } = "";
    public string Side { get; set; } = "";
    public int Quantity { get; set; }
    public decimal Price { get; set; }
}

public class Program
{
    public static void Main()
    {
        var trades = new List<Trade>
        {
            new Trade { Symbol = "AAPL", Side = "BUY",  Quantity = 100, Price = 180m },
            new Trade { Symbol = "AAPL", Side = "BUY",  Quantity = 200, Price = 170m },
            new Trade { Symbol = "MSFT", Side = "BUY",  Quantity = 300, Price = 160m },
            new Trade { Symbol = "TSLA", Side = "SELL", Quantity = 50,  Price = 250m },
            new Trade { Symbol = "GOOGL", Side = "BUY", Quantity = 10,  Price = 140m }
        };

        var result = trades
            .Where(t => t.Side == "BUY")
            .GroupBy(t => t.Symbol)
            .Select(g => (
                symbol: g.Key,
                vwap: g.Sum(t => t.Quantity * t.Price) / g.Sum(t => t.Quantity)
            ))
            .Where(x => x.vwap > 150.0m)
            .OrderBy(x => x.symbol)
            .ToList();

        foreach (var item in result)
        {
            Console.WriteLine($"{item.symbol}: {item.vwap:F2}");
        }
    }
}
