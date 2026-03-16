def inspect_string(text: str) -> None:
    utf8 = text.encode("utf-8")
    utf16 = text.encode("utf-16-le")

    print(f"Text: {text}")
    print(f"Characters: {len(text)}")
    print(f"UTF-8 bytes: {len(utf8)}")
    print(f"UTF-16 bytes: {len(utf16)}")
    print(f"UTF-8 hex: {utf8.hex()}")
    print()


samples = [
    "market",
    "café",
    "你好",
    "📈",
]

for sample in samples:
    inspect_string(sample)