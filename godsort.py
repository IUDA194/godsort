import random
import threading


def is_sorted(arr: list[int]) -> bool:
    """Проверка, что массив отсортирован неубывающе."""
    prev_el = arr[0]
    for el in arr[1:]:
        if prev_el > el:
            return False
        prev_el = el
    return True


def swamp_reset(arr: list[int]) -> list[int]:
    """Меняем местами два случайных элемента массива."""
    fr = random.randint(0, len(arr) - 1)
    sr = random.randint(0, len(arr) - 1)

    arr[fr], arr[sr] = arr[sr], arr[fr]
    return arr


def swamp_worker(
    thread_id: int,
    base_arr: list[int],
    stop_event: threading.Event,
    result_holder: dict,
    lock: threading.Lock,
    debug: bool = False,
):
    """
    Один поток: крутит свою копию массива до тех пор, пока:
    - не найдёт отсортированный вариант
    - или кто-то другой не закончит (stop_event)
    """
    local_arr = base_arr[:]  # своя копия массива

    while not stop_event.is_set():
        swamp_reset(local_arr)

        if is_sorted(local_arr):
            # Кто первый – того и тапки
            with lock:
                if not stop_event.is_set():
                    result_holder["result"] = local_arr[:]
                    result_holder["winner"] = thread_id
                    stop_event.set()
                    if debug:
                        print(f"[THREAD {thread_id}] нашёл решение:", local_arr)
            break

        if debug and random.random() < 0.0001:  # иногда лог, чтобы не засрать консоль
            print(f"[THREAD {thread_id}] текущий arr:", local_arr)


def parallel_swamp_sort(arr: list[int], num_threads: int = 100, debug: bool = False) -> list[int]:
    """
    Запускает num_threads потоков, каждый пытается отсортировать массив случайными свапами.
    Возвращает первый найденный отсортированный вариант.
    """
    stop_event = threading.Event()
    result_holder: dict = {}
    lock = threading.Lock()

    threads: list[threading.Thread] = []

    for i in range(num_threads):
        t = threading.Thread(
            target=swamp_worker,
            args=(i, arr, stop_event, result_holder, lock, debug),
            daemon=True,
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return result_holder.get("result", arr)


def main():
    N = 50
    arr: list[int] = [random.randrange(0, 100) for _ in range(N)]

    print("Исходный массив:", arr)
    sorted_arr = parallel_swamp_sort(arr, num_threads=500, debug=False)
    print("Отсортированный массив:", sorted_arr)


if __name__ == "__main__":
    main()
