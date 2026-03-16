def twos_complement(value: int, bits: int) -> str:
    mask = (1 << bits) - 1
    return format(value & mask, f"0{bits}b")


def show_representations(n: int) -> None:
    print(f"Integer: {n}")
    print(f"8-bit :  {twos_complement(n, 8)}")
    print(f"16-bit:  {twos_complement(n, 16)}")
    print(f"32-bit:  {twos_complement(n, 32)}")
    print()


test_values = [0, 1, 127, -1, -128, 255, 1000, -1000]

for value in test_values:
    show_representations(value)

# -1 is all 1s in two's complement because it is represented modulo 2^n.