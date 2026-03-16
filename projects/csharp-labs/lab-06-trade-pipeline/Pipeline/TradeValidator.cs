using TradePipeline.Models;

namespace TradePipeline.Pipeline;

public static class TradeValidator
{
    private static readonly HashSet<string> ValidSymbols =
        ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"];

    private const int    MinQuantity = 1;
    private const int    MaxQuantity = 1_000_000;
    private const double MinPrice    = 0.01;
    private const double MaxPrice    = 100_000.0;

    /// <summary>
    /// Returns null if valid, ValidationError if not.
    /// Pure function — no side effects.
    /// </summary>
    public static ValidationError? Validate(Trade trade)
    {
        if (!ValidSymbols.Contains(trade.Symbol))
            return new ValidationError(trade.TradeId,
                $"Unknown symbol '{trade.Symbol}'");

        if (trade.Quantity is < MinQuantity or > MaxQuantity)
            return new ValidationError(trade.TradeId,
                $"Quantity {trade.Quantity} out of range [{MinQuantity}, {MaxQuantity}]");

        if (trade.Price is < MinPrice or > MaxPrice)
            return new ValidationError(trade.TradeId,
                $"Price {trade.Price} out of range [{MinPrice}, {MaxPrice}]");

        return null; // valid
    }
}