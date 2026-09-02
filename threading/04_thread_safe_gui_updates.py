"""
Simulates the thread-safe GUI update pattern used by Tkinter-style apps:
background threads never touch the GUI directly - they push updates onto
a queue, and only the MAIN thread's event loop applies them.
"""
import threading
import queue
import time

# ===== SIMULATES the "GUI main thread" =====
# Tkinter has exactly this pattern internally - an 'event queue' where all
# updates get collected, and only the MAIN THREAD processes them

gui_update_queue = queue.Queue()


def fake_button_update(new_text):
    """Imagine this is a Tkinter button.config(text=...) call"""
    print(f"  [GUI UPDATED] Button text is now: '{new_text}'")


# ===== BACKGROUND THREAD - like a safe_process_runner =====
def background_worker():
    print("[Background Thread] Starting heavy work (fetching data from ERP)...")
    time.sleep(1)  # simulates a network call
    print("[Background Thread] Work done! Now need to update the GUI...")

    # WRONG WAY (this can crash/glitch in a real Tkinter app):
    # fake_button_update("Done!")   -- touching the GUI directly from a background thread is risky

    # CORRECT WAY: put the update on a queue, the MAIN THREAD will process it
    gui_update_queue.put(lambda: fake_button_update("Done!"))
    print("[Background Thread] Update queued, my work is done now")


# ===== MAIN THREAD - like root.mainloop() =====
def main_thread_event_loop():
    """
    Tkinter's root.mainloop() does exactly this internally:
    it repeatedly checks 'is there a pending GUI update?'
    If there is, it executes it from THIS thread (the main thread).
    """
    t1 = threading.Thread(target=background_worker, daemon=True)
    t1.start()
    t2 = threading.Thread(target=background_worker, daemon=True)
    t2.start()
    t1.join()
    t2.join()

    print("[Main Thread] Both workers finished, GUI stays responsive the whole time...")

    # This loop is a simplified version of root.mainloop()
    for _ in range(15):
        try:
            job = gui_update_queue.get(timeout=0.2)  # check the queue
            print("[Main Thread] Got a pending GUI update from the queue, applying it...")
            job()   # the actual GUI update happens here, from the MAIN THREAD
        except queue.Empty:
            pass  # nothing pending right now, keep the GUI responsive


main_thread_event_loop()
