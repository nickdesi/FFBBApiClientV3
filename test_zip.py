import time

queries = list(range(100000))
results = list(range(100000))


def f1():
    t0 = time.time()
    for _ in range(100):
        # mock mutate
        out = []
        for i, res in enumerate(results):
            q = queries[i]
            out.append(q + res)
    return time.time() - t0


def f2():
    t0 = time.time()
    for _ in range(100):
        [q + res for q, res in zip(queries, results)]
    return time.time() - t0


print("enumerate:", f1())
print("zip list comp:", f2())
