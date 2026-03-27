using System;
using System.Collections.Generic;
using System.Linq;

public class Trade
{
    public string Symbol { get; set; } = "";
    public string Side { get; set; } = "";
    public int Quantity { get; set; }
    public decimal Price { get; set; }
    public decimal Notional => Quantity * Price;
}

public static class TradeExtensions
{
    public static decimal TotalNotional(this IEnumerable<Trade> trades) =>
        trades.Sum(t => t.Notional);

    public static decimal AveragePrice(this IEnumerable<Trade> trades) =>
        trades.Any() ? trades.Average(t => t.Price) : 0m;

    public static Trade? LargestTrade(this IEnumerable<Trade> trades) =>
        trades.OrderByDescending(t => t.Notional).FirstOrDefault();

    public static (IEnumerable<Trade> buys, IEnumerable<Trade> sells) SplitBySide(
        this IEnumerable<Trade> trades
    ) =>
        (
            trades.Where(t => t.Side == "BUY"),
            trades.Where(t => t.Side == "SELL")
        );
}

public class Program
{
    public static void Main()
    {
        var trades = new List<Trade>
        {
            new Trade { Symbol = "AAPL", Side = "BUY",  Quantity = 100, Price = 180m },
            new Trade { Symbol = "MSFT", Side = "SELL", Quantity = 50,  Price = 420m },
            new Trade { Symbol = "GOOGL", Side = "BUY", Quantity = 10,  Price = 2200m },
            new Trade { Symbol = "AAPL", Side = "SELL", Quantity = 75,  Price = 182m }
        };

        Console.WriteLine($"Total notional: {trades.TotalNotional()}");
        Console.WriteLine($"Average price: {trades.AveragePrice()}");

        var largest = trades.LargestTrade();
        Console.WriteLine($"Largest trade: {largest?.Symbol} {largest?.Side} {largest?.Notional}");

        var (buys, sells) = trades.SplitBySide();
        Console.WriteLine($"Buy count: {buys.Count()}");
        Console.WriteLine($"Sell count: {sells.Count()}");
    }
}