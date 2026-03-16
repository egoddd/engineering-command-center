using System;
using System.Runtime.InteropServices;

[StructLayout(LayoutKind.Sequential)]
struct TradeA
{
	public long TradeId;
	public double Price;
	public int Quantity;
	public byte Side;
	public bool Isfilled;
}

[StructLayout(LayoutKind.Sequential)]
struct TradeB
{
	public byte Side;
	public bool IsFilled;
	public int Quantity;
	public long TradeId;
	public double Price;
}

[StructLayout(LayoutKind.Sequential)]
struct TradeC
{
	public long TradeId;
	public int Quantity;
	public bool IsFilled;
	public double Price;
}

class Program
{
	static void Main()
	{
		Console.WriteLine($"TradeA size: {Marshal.SizeOf<TradeA>()}");
		Console.WriteLine($"TradeB size: {Marshal.SizeOf<TradeB>()}");
		Console.WriteLine($"TradeC size: {Marshal.SizeOf<TradeC>()}");
	}
}