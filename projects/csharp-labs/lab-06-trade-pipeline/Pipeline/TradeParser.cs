using System.Globalization;
using TradePipeline.Models;

namespace TradePipeline.Pipeline;

public static class TradeParser
{
    /// <summary>
    /// Lazily parses trades from a CSV file using an iterator method.
    /// Connects to Day 5: yield return suspends the method frame between records.
    /// Memory efficient — one record in memory at a time during parsing.
    /// </summary>
    public static IEnumerable<object> ParseTrades(string filepath)
    {
        if (!File.Exists(filepath))
        {
            Console.Error.WriteLine($"Error: file not found: {filepath}");
            yield break;
        }

        using var reader = new StreamReader(filepath);

        // Skip header
        var header = reader.ReadLine();
        if (header is null) yield break;

        string? line;
        while ((line = reader.ReadLine()) is not null)
        {
            var parts = line.Split(',');
            if (parts.Length < 6) continue;

            var tradeId = parts[0].Trim();

            // Try to parse — yield ValidationError on failure
            if (!int.TryParse(parts[3].Trim(), out int quantity))
            {
                yield return new ValidationError(tradeId,
                    $"Invalid quantity: '{parts[3].Trim()}'");
                continue;
            }

            if (!double.TryParse(parts[4].Trim(),
                    NumberStyles.Float,
                    CultureInfo.InvariantCulture,
                    out double price))
            {
                yield return new ValidationError(tradeId,
                    $"Invalid price: '{parts[4].Trim()}'");
                continue;
            }

            if (!DateTime.TryParseExact(parts[5].Trim(),
                    "yyyy-MM-dd HH:mm:ss",
                    CultureInfo.InvariantCulture,
                    DateTimeStyles.None,
                    out DateTime timestamp))
            {
                yield return new ValidationError(tradeId,
                    $"Invalid timestamp: '{parts[5].Trim()}'");
                continue;
            }

            // Parse side — don't throw, yield error instead
            if (!Enum.TryParse<TradeSide>(parts[2].Trim().ToUpper(),
                    out TradeSide side))
            {
                yield return new ValidationError(tradeId,
                    $"Invalid side: '{parts[2].Trim()}'");
                continue;
            }

            yield return new Trade(
                TradeId:   tradeId,
                Symbol:    parts[1].Trim(),
                Side:      side,
                Quantity:  quantity,
                Price:     price,
                Timestamp: timestamp
            );
        }
    }
}