# cat << 'EOF' > /home/claude/no_threading.py
import time

def heavy_task(name, duration):
    print(f"[{name}] Kaam shuru...")
    time.sleep(duration)   # yeh simulate karta hai "heavy work" - jaise network call ya file processing
    print(f"[{name}] Kaam khatam!")

print("=== BINA THREADING KE ===")
start = time.time()

heavy_task("Task-A", 2)
heavy_task("Task-B", 2)

print(f"Total time liya: {round(time.time() - start, 2)} seconds")
# EOF
# python3 /home/claude/no_threading.py
# Output

# === BINA THREADING KE ===
# [Task-A] Kaam shuru...
# [Task-A] Kaam khatam!
# [Task-B] Kaam shuru...
# [Task-B] Kaam khatam!
# Total time liya: 4.0 seconds