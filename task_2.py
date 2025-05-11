import timeit
from functools import lru_cache
from tabulate import tabulate
import matplotlib.pyplot as plt

from cache_splay_tree import st_cache


@lru_cache
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


@st_cache
def fibonacci_splay(n):
    if n < 2:
        return n
    return fibonacci_splay(n - 1) + fibonacci_splay(n - 2)


if __name__ == '__main__':
    nums = range(0, 1000, 50)

    results = [
        (n, timeit.timeit(lambda: fibonacci_lru(n), number=100), timeit.timeit(lambda: fibonacci_splay(n), number=1))
        for n in nums
    ]

    table = tabulate(results, headers=['n', 'LRU Cache Time (s)', 'Splay Tree Time (s)'])
    print(table)

    lru_results = [float(r[1]) for r in results]
    st_results = [float(r[2]) for r in results]

    plt.plot(nums, lru_results, '-o', label='LRU Cache')
    plt.plot(nums, st_results, '-s', label='Splay Tree')
    plt.title("Порівняння часу виконання LRU Cache та Splay Tree")
    plt.xlabel("Число Фібоначчі (n)")
    plt.ylabel("Середній час виконання (секунди)")
    plt.legend()
    plt.grid()
    plt.show()
