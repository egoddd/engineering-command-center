using System;

public record Trade(string Side, int Quantity);

public static class TradeClassifier
{
    public static string ClassifyTrade(Trade trade) =>
        trade switch
        {
            { Side: "BUY", Quantity: > 500 }  => "large-buy",
            { Side: "SELL", Quantity: > 500 } => "large-sell",
            { Side: "BUY", Quantity: <= 500 } => "small-buy",
            { Side: "SELL", Quantity: <= 500 } => "small-sell",
            _ => "invalid"
        };

    public static void Main()
    {
        var trades = new[]
        {
            new Trade("BUY", 100),
            new Trade("BUY", 900),
            new Trade("SELL", 50),
            new Trade("SELL", 700),
            new Trade("HOLD", 100),
            new Trade("BUY", -1)
        };

        foreach (var trade in trades)
        {
            Console.WriteLine($"{trade} -> {ClassifyTrade(trade)}");
        }
    }
}