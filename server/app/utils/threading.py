import threading
import time


def threading_task(func, args, times=None):
    if times != None:
        threads = []

        for _ in range(times):
            t = threading.Thread(target=func, args=[args])
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()
    else:
        thread = threading.Thread(target=func, args=[args])
        thread.start()
        thread.join()


if __name__ == "__main__":
    start = time.perf_counter()

    def do_something(seconds):
        print(f'Sleeping in {seconds} second(s)...')
        time.sleep(seconds)
        print(f'Done sleeping...')

    threading_task(do_something, 2, times=3)

    # threads = []

    # for _ in range(10):
    #     t = threading.Thread(target=do_something, args=[2])
    #     t.start()
    #     threads.append(t)

    # for thread in threads:
    #     thread.join()

    finish = time.perf_counter()

    print(f"Finished in {round(finish-start, 2)} seconds")
