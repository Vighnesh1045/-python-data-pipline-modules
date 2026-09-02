# cat << 'EOF' > /home/claude/race_condition.py
import threading

# ===== Shared variable - dono threads isi ek cheez ko modify karenge =====
counter = 0

def increment_many_times():
    global counter
    for _ in range(100000):
        counter = counter + 1   # yeh line teen steps mein hoti hai internally (niche samjhata hoon)

# Do threads banaye, dono SAME counter ko increment kar rahe hain
t1 = threading.Thread(target=increment_many_times)
t2 = threading.Thread(target=increment_many_times)

t1.start()
print("start t1")
t2.start()
print("start t2")
# t1.join()
# print("wait t1")
# t2.join()
# print("wait t12")

print(f"Expected value: 200000")
print(f"Actual value:   {counter}")
print(f"Kitna 'lost' ho gaya: {200000 - counter}")
# EOF
# python3 /home/claude/race_condition.py
# Output

# Expected value: 200000
# Actual value:   200000
# Kitna 'lost' ho gaya: 0