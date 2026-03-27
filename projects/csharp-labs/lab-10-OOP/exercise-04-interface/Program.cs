using System;
using System.Collections.Generic;

public class Order
{
    public string Symbol { get; set; } = "";
    public int Quantity { get; set; }
    public decimal Price { get; set; }
    public int PositionAfter { get; set; }
}

public interface IRiskCheck
{
    string Name { get; }
    bool Check(Order order);
}

public class PositionLimitCheck : IRiskCheck
{
    private readonly int _maxPosition;
    public string Name => "PositionLimitCheck";

    public PositionLimitCheck(int maxPosition)
    {
        _maxPosition = maxPosition;
    }

    public bool Check(Order order) => Math.Abs(order.PositionAfter) <= _maxPosition;
}

public class NotionalLimitCheck : IRiskCheck
{
    private readonly decimal _maxNotional;
    public string Name => "NotionalLimitCheck";

    public NotionalLimitCheck(decimal maxNotional)
    {
        _maxNotional = maxNotional;
    }

    public bool Check(Order order) => Math.Abs(order.Quantity * order.Price) <= _maxNotional;
}

public class SymbolAllowlistCheck : IRiskCheck
{
    private readonly HashSet<string> _allowedSymbols;
    public string Name => "SymbolAllowlistCheck";

    public SymbolAllowlistCheck(IEnumerable<string> allowedSymbols)
    {
        _allowedSymbols = new HashSet<string>(allowedSymbols);
    }

    public bool Check(Order order) => _allowedSymbols.Contains(order.Symbol);
}

public class RiskEngine
{
    private readonly IEnumerable<IRiskCheck> _checks;

    public RiskEngine(IEnumerable<IRiskCheck> checks)
    {
        _checks = checks;
    }

    public (bool success, string? failedCheck) Run(Order order)
    {
        foreach (var check in _checks)
        {
            if (!check.Check(order))
            {
                return (false, check.Name);
            }
        }

        return (true, null);
    }
}

public class Program
{
    public static void Main()
    {
        var checks = new List<IRiskCheck>
        {
            new PositionLimitCheck(1000),
            new NotionalLimitCheck(100000m),
            new SymbolAllowlistCheck(new[] { "AAPL", "MSFT", "GOOGL" })
        };

        var engine = new RiskEngine(checks);

        var order = new Order
        {
            Symbol = "AAPL",
            Quantity = 100,
            Price = 180m,
            PositionAfter = 500
        };

        var result = engine.Run(order);
        Console.WriteLine($"Success: {result.success}, FailedCheck: {result.failedCheck}");
    }
}