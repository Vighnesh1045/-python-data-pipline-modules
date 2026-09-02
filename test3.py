# cat << 'EOF' > /home/claude/daemon_example.py
import threading
import time

def background_worker():
    print("Background worker shuru hua...")
    time.sleep(5)   # yeh 5 second ka kaam hai
    print("Yeh line kabhi print nahi hogi agar main program pehle hi exit ho gaya")

# daemon=True ka matlab: yeh thread "background helper" hai
# Agar MAIN program khatam ho jaaye, toh yeh thread bhi FORCE-KILL ho jayegi
t = threading.Thread(target=background_worker, daemon=True)
t.start()
# t.join()
print("Main program ka kaam khatam, ab exit kar raha hoon...")
# Note: humne .join() nahi lagaya, isliye main program turant exit ho jayega
# aur daemon thread ko poora hone ka mauka nahi milega
# EOF
# python3 /home/claude/daemon_example.py
# Output

# Main program ka kaam khatam, ab exit kar raha hoon...
# Background worker shuru hua...