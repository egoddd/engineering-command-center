import dis

def sum_positive_even(numbers):
    total = 0

    for n in numbers:           # loop over list
        if n > 0 and n % 2 == 0:   # condition check
            total += n

    return total


dis.dis(sum_positive_even)