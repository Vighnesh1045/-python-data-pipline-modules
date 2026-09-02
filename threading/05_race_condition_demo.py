"""
A race condition demo with a simple shared counter incremented by two
threads. Note this script deliberately skips t1.join()/t2.join() before
printing the result, so the printed count can reflect a still-in-progress
computation - run it a few times and watch the "Actual value" vary.
"""
import threading

# Shared variable - both threads modify this same variable
counter = 0


def increment_many_times():
    global counter
    for _ in range(100000):
        counter = counter + 1   # this line actually happens in three steps internally


# Create two threads, both incrementing the SAME counter
t1 = threading.Thread(target=increment_many_times)
t2 = threading.Thread(target=increment_many_times)

t1.start()
print("start t1")
t2.start()
print("start t2")
# t1.join()
# print("wait t1")
# t2.join()
# print("wait t2")

print("Expected value: 200000")
print(f"Actual value:   {counter}")
print(f"Lost due to race condition / still in progress: {200000 - counter}")
