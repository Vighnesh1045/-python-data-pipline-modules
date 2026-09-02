"""
Demonstrates a race condition made GUARANTEED (via time.sleep between
read/modify/write) and how threading.Lock fixes it.
"""
import threading
import time

counter = 0


def unsafe_increment():
    global counter
    for _ in range(5):
        # This manually breaks "counter = counter + 1" into 3 steps
        # so the race condition is GUARANTEED to show (in the real world these
        # 3 steps happen so fast that seeing a race normally depends on luck)

        current_value = counter        # STEP 1: READ
        time.sleep(0.001)              # <-- another thread can jump in here!
        new_value = current_value + 1  # STEP 2: CALCULATE
        counter = new_value            # STEP 3: WRITE back


def safe_increment(lock):
    global counter
    for _ in range(5):
        with lock:   # <-- LOCK acquired - only ONE thread can be inside this block at a time
            current_value = counter
            time.sleep(0.001)
            new_value = current_value + 1
            counter = new_value


print("===== WITHOUT A LOCK (UNSAFE) =====")
counter = 0
threads = [threading.Thread(target=unsafe_increment) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()
print(f"Expected: 20, Actual: {counter}  <-- LOST UPDATES!\n")


print("===== WITH A LOCK (SAFE) =====")
counter = 0
my_lock = threading.Lock()
threads = [threading.Thread(target=safe_increment, args=(my_lock,)) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()
print(f"Expected: 20, Actual: {counter}  <-- Correct!")
