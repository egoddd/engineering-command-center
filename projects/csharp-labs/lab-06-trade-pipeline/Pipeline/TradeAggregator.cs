using TradePipeline.Models;

namespace TradePipeline.Pipeline;

public class SymbolStats
{
    public string Symbol      { get; init; } = "";
    public int    TradeCount  { get; private set; }
    public int    TotalVolume { get; private set; }
    public double TotalNotional { get; private set; }
    public int    BuyCount    { get; private set; }
    public int    SellCount   { get; private set; }
    public double MinPrice    { get; private set; } = double.MaxValue;
    public double MaxPrice    { get; private set; } = double.MinValue;

    // Volume-Weighted Average Price
    public double Vwap => TotalVolume > 0
        ? TotalNotional / TotalVolume
        : 0.0;

    public void Apply(Trade trade)
    {
        TradeCount++;
        TotalVolume   += trade.Quantity;
        TotalNotional += trade.Notional;
        MinPrice       = Math.Min(MinPrice, trade.Price);
        MaxPrice       = Math.Max(MaxPrice, trade.Price);

        if (trade.Side == TradeSide.BUY) BuyCount++;
        else SellCount++;
    }
}

public static class TradeAggregator
{
    public static Dictionary<string, SymbolStats> Aggregate(
        IEnumerable<Trade> trades)
    {
        var stats = new Dictionary<string, SymbolStats>();

        foreach (var trade in trades)
        {
            if (!stats.TryGetValue(trade.Symbol, out var s))
            {
                s = new SymbolStats { Symbol = trade.Symbol };
                stats[trade.Symbol] = s;
            }
            s.Apply(trade);
        }

        return stats;
    }
}