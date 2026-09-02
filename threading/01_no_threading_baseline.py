"""
Baseline demo: running two "heavy" tasks sequentially, without threading.
Each task blocks the next one from starting, so total time is additive.
"""
import time


def heavy_task(name, duration):
    print(f"[{name}] Starting work...")
    time.sleep(duration)  # simulates "heavy work" - e.g. a network call or file processing
    print(f"[{name}] Work done!")


print("=== WITHOUT THREADING ===")
start = time.time()

heavy_task("Task-A", 2)
heavy_task("Task-B", 2)

print(f"Total time taken: {round(time.time() - start, 2)} seconds")
