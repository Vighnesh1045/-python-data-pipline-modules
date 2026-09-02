# cat << 'EOF' > /home/claude/race_condition_v2.py
import threading
import time

counter = 0

def unsafe_increment():
    global counter
    for _ in range(5):
        # yeh ek "counter = counter + 1" ko manually 3 steps mein tod diya hai
        # taaki race condition GUARANTEED dikhe (real duniya mein yeh 3 steps
        # itni tezi se hote hain ki normally race dikhna luck pe depend karta hai)

        current_value = counter        # STEP 1: READ karo
        time.sleep(0.001)              # <-- yahan doosra thread beech mein aa sakta hai!
        new_value = current_value + 1  # STEP 2: CALCULATE karo
        counter = new_value            # STEP 3: WRITE karo wapas

def safe_increment(lock):
    global counter
    for _ in range(5):
        with lock:   # <-- LOCK lagaya - ab sirf EK thread is block ke andar aa sakta hai
            current_value = counter
            time.sleep(0.001)
            new_value = current_value + 1
            counter = new_value


print("===== BINA LOCK KE (UNSAFE) =====")
counter = 0
threads = [threading.Thread(target=unsafe_increment) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()
print(f"Expected: 20, Actual: {counter}  <-- LOST UPDATES!\n")


print("===== LOCK KE SAATH (SAFE) =====")
counter = 0
my_lock = threading.Lock()
threads = [threading.Thread(target=safe_increment, args=(my_lock,)) for _ in range(4)]
for t in threads: t.start()
for t in threads: t.join()
print(f"Expected: 20, Actual: {counter}  <-- Sahi hai!")
# EOF
# python3 /home/claude/race_condition_v2.py
# Output

# ===== BINA LOCK KE (UNSAFE) =====
# Expected: 20, Actual: 5  <-- LOST UPDATES!

# ===== LOCK KE SAATH (SAFE) =====
# Expected: 20, Actual: 20  <-- Sahi hai!