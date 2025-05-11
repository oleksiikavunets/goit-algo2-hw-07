import random
import timeit

from cache_lru import LRUCache


def count_sum(array, L, R):
    return sum(array[L:R + 1])


def range_sum_no_cache(array, L, R):
    return count_sum(array, L, R)


def update_no_cache(array, index, value):
    array[index] = value


lru = LRUCache(1000)


def range_sum_with_cache(array, L, R):
    key = f'{L}-{R}'
    if not lru.contains(key):
        result = count_sum(array, L, R)
        lru.put(key, result)
    return lru.get(key)


def update_with_cache(array, index, value):
    array[index] = value

    for k in lru.cache.keys():
        L, R = [int(i) for i in k.split('-')]

        if L >= index >= R:
            lru.remove(k)


if __name__ == '__main__':
    rand_array = [random.randint(0, 100_000) for _ in range(100_000)]

    rand_calls = [
                     (random.choice(['Range', 'Update']), *sorted((random.randint(0, 99999), random.randint(0, 99999))))
                     for _ in range(5)
                 ] * 10000

    no_cache_start = timeit.default_timer()

    [
        (update_no_cache if call[0] == 'Update' else range_sum_no_cache)(rand_array, call[1], call[2])
        for call in rand_calls
    ]

    no_cache_time = timeit.default_timer() - no_cache_start

    cache_start = timeit.default_timer()

    [
        (update_with_cache if call[0] == 'Update' else range_sum_with_cache)(rand_array, call[1], call[2])
        for call in rand_calls
    ]

    cache_time = timeit.default_timer() - cache_start

    print(f'Час виконання без кешування: {no_cache_time} секунд')
    print(f'Час виконання з LRU-кешем: {cache_time} секунд')

    # Час виконання без кешування: 13.277897082996788 секунд
    # Час виконання з LRU-кешем: 0.034903958992799744 секунд
