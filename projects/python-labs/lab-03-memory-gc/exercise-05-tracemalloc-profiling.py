import tracemalloc

def build_data():
    data = []
    for i in range(100_000):
        data.append({"value": i, "text": str(i)})
    return data

tracemalloc.start()

snapshot1 = tracemalloc.take_snapshot()

data = build_data()

snapshot2 = tracemalloc.take_snapshot()

top_stats = snapshot2.compare_to(snapshot1, 'lineno')

print("Top 5 allocation sites:")
for stat in top_stats[:5]:
    print(stat)