"""
Demonstrates atexit: registering a cleanup function that automatically
runs when the program exits, without being called explicitly.
"""
import atexit


def cleanup_function():
    print("Cleaning up... deleting the lock file, closing connections.")


# This REGISTERS the function - cleanup_function() does NOT run yet.
# It just tells Python "run this when the program exits".
atexit.register(cleanup_function)

print("Program is doing its normal work...")
print("Program is ending now...")

# Note: we never called cleanup_function() manually.
# It still runs automatically when the script ends.
