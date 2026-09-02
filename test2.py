# cat << 'EOF' > /home/claude/with_threading.py
import threading
import time

def heavy_task(name, duration):
    print(f"[{name}] Kaam shuru...")
    time.sleep(duration)
    print(f"[{name}] Kaam khatam!")

print("=== THREADING KE SAATH ===")
start = time.time()

# Thread object banaya - target = konsa function chalana hai, args = uske parameters
t1 = threading.Thread(target=heavy_task, args=("Task-A", 2))
t2 = threading.Thread(target=heavy_task, args=("Task-B", 2))

t1.start()   # thread ko chalu karo (background mein)
t2.start()   # yeh bhi turant chalu ho jayega, t1 ke khatam hone ka wait nahi karega

t1.join()    # 'join' ka matlab: "main (main program) yahan ruk jaunga jab tak t1 khatam na ho"
t2.join()

print(f"Total time liya: {round(time.time() - start, 2)} seconds")
# EOF
# python3 /home/claude/with_threading.py
# Output

# === THREADING KE SAATH ===
# [Task-A] Kaam shuru...
# [Task-B] Kaam shuru...
# [Task-A] Kaam khatam!
# [Task-B] Kaam khatam!
# Total time liya: 2.0 seconds