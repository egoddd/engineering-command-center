using TradePipeline.Models;
using TradePipeline.Pipeline;

// ─────────────────────────────────────────────────────
// PIPELINE ORCHESTRATOR
// Connects all stages: parse → validate → transform
//                      → aggregate → report
// ─────────────────────────────────────────────────────

string filepath = args.Length > 0 ? args[0] : "trades.csv";

var validTrades   = new List<Trade>();
var invalidTrades = new List<ValidationError>();
int totalParsed   = 0;

// Stage 1 + 2: parse and validate
// ParseTrades is an iterator — one record at a time, like Python generator
foreach (var record in TradeParser.ParseTrades(filepath))
{
    totalParsed++;

    if (record is ValidationError parseError)
    {
        invalidTrades.Add(parseError);
        continue;
    }

    if (record is Trade trade)
    {
        var validationError = TradeValidator.Validate(trade);
        if (validationError is not null)
        {
            invalidTrades.Add(validationError);
            continue;
        }

        validTrades.Add(trade);
    }
}

// Stage 3: aggregate
var stats = TradeAggregator.Aggregate(validTrades);

// Stage 4: report
PrintReport();

// ─────────────────────────────────────────────────────
// REPORT
// ─────────────────────────────────────────────────────

void PrintReport()
{
    const int width = 60;
    var line = new string('=', width);
    var dash = new string('─', width);

    Console.WriteLine(line);
    Console.WriteLine("  TRADE PIPELINE REPORT");
    Console.WriteLine(line);

    Console.WriteLine($"\n  {"Total records parsed:",-30} {totalParsed}");
    Console.WriteLine($"  {"Valid trades:",-30} {validTrades.Count}");
    Console.WriteLine($"  {"Rejected trades:",-30} {invalidTrades.Count}");

    if (invalidTrades.Count > 0)
    {
        Console.WriteLine($"\n{dash}");
        Console.WriteLine("  REJECTED TRADES");
        Console.WriteLine(dash);
        foreach (var err in invalidTrades)
            Console.WriteLine($"  [{err.TradeId}] {err.Reason}");
    }

    Console.WriteLine($"\n{dash}");
    Console.WriteLine("  SYMBOL STATISTICS");
    Console.WriteLine(dash);
    Console.WriteLine($"  {"Symbol",-8} {"Trades",6} {"Volume",8} " +
                      $"{"VWAP",10} {"Min",8} {"Max",8} {"Buy/Sell",10}");
    Console.WriteLine($"  {"─────────",-8} {"──────",6} {"────────",8} " +
                      $"{"──────────",10} {"────────",8} {"────────",8}");

    foreach (var (symbol, s) in stats.OrderBy(x => x.Key))
    {
        Console.WriteLine($"  {s.Symbol,-8} {s.TradeCount,6} {s.TotalVolume,8} " +
                          $"${s.Vwap,9:F2} ${s.MinPrice,7:F2} " +
                          $"${s.MaxPrice,7:F2} " +
                          $"{s.BuyCount}B/{s.SellCount}S");
    }

    double totalNotional = stats.Values.Sum(s => s.TotalNotional);
    int    totalVolume   = stats.Values.Sum(s => s.TotalVolume);

    Console.WriteLine(dash);
    Console.WriteLine($"\n  {"Total notional traded:",-30} ${totalNotional:N2}");
    Console.WriteLine($"  {"Total shares traded:",-30} {totalVolume:N0}");
    Console.WriteLine($"\n{line}\n");
}