"""
Demonstrates daemon threads: a background thread that gets force-killed
the moment the main program exits, instead of being waited on.
"""
import threading
import time


def background_worker():
    print("Background worker started...")
    time.sleep(5)   # simulates 5 seconds of work
    print("This line will never print if the main program already exited")


# daemon=True means this thread is a "background helper" -
# if the MAIN program ends, this thread gets FORCE-KILLED along with it
t = threading.Thread(target=background_worker, daemon=True)
t.start()
# t.join()
print("Main program's work is done, exiting now...")
# Note: we didn't call .join(), so the main program exits immediately
# and the daemon thread never gets a chance to finish
