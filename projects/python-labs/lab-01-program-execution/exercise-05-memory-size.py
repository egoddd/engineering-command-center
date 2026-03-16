import sys

items = {
    "int": 42,
    "float": 3.14,
    "empty_list": [],
    "list_10_ints": list(range(10)),
    "empty_dict": {},
    "str_len_5": "hello",
}

for name, value in items.items():
    print(f"{name}: {sys.getsizeof(value)} bytes")