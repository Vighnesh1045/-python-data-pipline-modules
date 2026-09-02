"""
Shows that atexit-registered cleanup functions still run even when the
program crashes with an unhandled exception.
"""
import atexit


def cleanup_function():
    print("Cleaning up, whether it crashed or not!")


atexit.register(cleanup_function)

print("Program started...")
print("Now deliberately causing an error...")

result = 10 / 0   # this crashes (ZeroDivisionError)

print("This line will never print")   # unreachable because of the crash
