import random

def is_sorted(arr : list[int]):
    prev_el = 0
    for el in arr:
        if prev_el > el:
            return False
        prev_el = el

    return True


def swamp_reset(arr: list[int]):
    fr = random.randint(0, len(arr) - 1)
    sr = random.randint(0, len(arr) - 1)

    tmp = arr[sr]

    arr[sr] = arr[fr]
    arr[fr] = tmp

    return arr


def swamp_sort(arr: list[int]):
    arr = swamp_reset(arr)
    while not is_sorted(arr):
        print("Arr: ", arr)
        arr = swamp_reset(arr)
    return arr


def main():
    N = 20

    arr = []

    for _ in range(N):
        arr.append(random.randrange(0, 100))

    print(swamp_sort(arr))


if __name__ == "__main__":
    main()
