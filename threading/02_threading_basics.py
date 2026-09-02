"""
Same two "heavy" tasks as the baseline demo, but run concurrently with
threading.Thread so the total time is roughly the duration of the
longest task instead of the sum of both.
"""
import threading
import time


def heavy_task(name, duration):
    print(f"[{name}] Starting work...")
    time.sleep(duration)
    print(f"[{name}] Work done!")


print("=== WITH THREADING ===")
start = time.time()

# Create Thread objects - target = which function to run, args = its parameters
t1 = threading.Thread(target=heavy_task, args=("Task-A", 2))
t2 = threading.Thread(target=heavy_task, args=("Task-B", 2))

t1.start()   # start the thread (runs in the background)
t2.start()   # this also starts immediately, it doesn't wait for t1 to finish

t1.join()    # 'join' means: "the main program will pause here until t1 finishes"
t2.join()

print(f"Total time taken: {round(time.time() - start, 2)} seconds")
