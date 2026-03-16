namespace TradePipeline.Models;

public enum TradeSide { BUY, SELL }

public record Trade(
    string    TradeId,
    string    Symbol,
    TradeSide Side,
    int       Quantity,
    double    Price,
    DateTime  Timestamp
)
{
    // Derived field — calculated after construction
    public double Notional { get; init; } = Quantity * Price;
}

public record ValidationError(string TradeId, string Reason);

public record PipelineResult(
    List<Trade>           ValidTrades,
    List<ValidationError> InvalidTrades,
    int                   TotalParsed
);