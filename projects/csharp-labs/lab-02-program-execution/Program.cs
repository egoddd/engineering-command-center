using System;

class ExecutionModel
{
    // Value type — lives on the stack when declared as a local variable
    struct Point
    {
        public int X;
        public int Y;
    }

    // Reference type — always lives on the heap
    class Rectangle
    {
        public int Width;
        public int Height;
    }

    static void DemonstrateMemory()
    {
        // Stack allocated — fast, automatic cleanup
        int counter = 0;         // 4 bytes on stack
        double temperature = 98.6; // 8 bytes on stack
        Point p = new Point { X = 3, Y = 7 }; // 8 bytes on stack — struct is value type

        // Heap allocated — CLR manages lifetime
        Rectangle rect = new Rectangle { Width = 10, Height = 20 }; // on the heap
        // 'rect' is a reference (like a pointer) — the reference itself is on the stack
        // The actual Rectangle object is on the heap

        Console.WriteLine($"counter: {counter}");
        Console.WriteLine($"Point: ({p.X}, {p.Y})");
        Console.WriteLine($"Rectangle: {rect.Width}x{rect.Height}");

    } // When this method returns:
      // counter, temperature, p are instantly gone (stack frame popped)
      // rect's reference is gone — Rectangle on heap is eligible for GC

    static int AddNumbers(int a, int b)
    {
        // a and b are passed on the stack
        int result = a + b; // result lives on the stack
        return result;      // return value passed via register or stack
    } // Stack frame popped — result gone

    static void Main()
    {
        DemonstrateMemory();

        int sum = AddNumbers(3, 4);
        Console.WriteLine($"Sum: {sum}");
    }
}