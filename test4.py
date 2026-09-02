# cat << 'EOF' > /home/claude/thread_safety_concept.py
import threading
import queue
import time

# ===== YEH SIMULATE KARTA HAI "GUI KA MAIN THREAD" =====
# Tkinter ke andar bhi bilkul yehi pattern hota hai - ek 'event queue' jisme
# saare updates jaake jama hote hain, aur MAIN THREAD hi unhe process karta hai

gui_update_queue = queue.Queue()

def fake_button_update(new_text):
    """Yeh imagine karo ek Tkinter button.config(text=...) hai"""
    print(f"  [GUI UPDATED] Button ka text ab hai: '{new_text}'")

# ===== BACKGROUND THREAD - jaise tumhara safe_process_runner =====
def background_worker():
    print("[Background Thread] Heavy kaam shuru (ERP se data fetch ho raha hai)...")
    time.sleep(1)  # simulate karo network call
    print("[Background Thread] Kaam khatam! Ab GUI update karni hai...")

    # ❌ GALAT TARIKA (yeh crash/glitch kar sakta hai real Tkinter mein):
    # fake_button_update("Done!")   -- seedha background thread se GUI touch karna risky hai

    # ✅ SAHI TARIKA: update ko ek queue mein daal do, MAIN THREAD process karega
    gui_update_queue.put(lambda: fake_button_update("Done!"))
    print("[Background Thread] Maine update queue mein daal diya, ab mera kaam khatam")


# ===== MAIN THREAD - jaise tumhara root.mainloop() =====
def main_thread_event_loop():
    """
    Tkinter ka root.mainloop() bilkul yehi karta hai internally:
    baar-baar check karta hai 'koi pending GUI update hai kya?'
    Agar hai, to USI thread se (main thread se) use execute karta hai.
    """
    t1 = threading.Thread(target=background_worker, daemon=True)
    t1.start()
    t2 = threading.Thread(target=background_worker,daemon = True)
    t2.start()
    t1.join()
    t2.join()

    print("[Main Thread] Main free hoon, GUI responsive hai, user kuch bhi kar sakta hai...")

    # Yeh loop root.mainloop() ka simplified version hai
    for _ in range(15):
        try:
            job = gui_update_queue.get(timeout=0.2)  # queue check karo
            print("[Main Thread] Mujhe ek pending GUI update mila queue mein, main karta hoon...")
            job()   # yahan actual GUI update MAIN THREAD se ho raha hai
        except queue.Empty:
            pass  # koi update nahi hai abhi, GUI responsive rehne do

main_thread_event_loop()
# EOF
# python3 /home/claude/thread_safety_concept.py
# Output

# [Main Thread] Main free hoon, GUI responsive hai, user kuch bhi kar sakta hai...
# [Background Thread] Heavy kaam shuru (ERP se data fetch ho raha hai)...
# [Background Thread] Kaam khatam! Ab GUI update karni hai...
# [Main Thread] Mujhe ek pending GUI update mila queue mein, main karta hoon...
#   [GUI UPDATED] Button ka text ab hai: 'Done!'
# [Background Thread] Maine update queue mein daal diya, ab mera kaam khatam