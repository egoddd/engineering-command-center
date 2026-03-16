import multiprocessing

def partial_sum(start: int, end: int, queue):
    total = sum(range(start, end + 1))
    queue.put(total)

def main():
    queue = multiprocessing.Queue()

    p1 = multiprocessing.Process(target=partial_sum, args=(1, 5_000_000, queue))
    p2 = multiprocessing.Process(target=partial_sum, args=(5_000_001, 10_000_000, queue))

    p1.start()
    p2.start()

    result1 = queue.get()
    result2 = queue.get()

    p1.join()
    p2.join()

    total = result1 + result2
    print(f"Combined total: {total}")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()