# cat << 'EOF' > /home/claude/atexit_example.py
import atexit

def cleanup_function():
    print("🧹 Cleanup ho raha hai... lock file delete kar raha hoon, connections band kar raha hoon.")

# Yeh REGISTER karta hai - abhi cleanup_function() CHALTA NAHI hai
# Bas Python ko bata diya "jab program exit ho, isse chala dena"
atexit.register(cleanup_function)

print("Program apna normal kaam kar raha hai...")
print("Ab program khatam ho raha hai...")

# Note: humne cleanup_function() ko kahin manually call nahi kiya
# Phir bhi yeh automatically chalega jab script end hogi
# EOF
# python3 /home/claude/atexit_example.py
# Output

# Program apna normal kaam kar raha hai...
# Ab program khatam ho raha hai...
# 🧹 Cleanup ho raha hai... lock file delete kar raha hoon, connections band kar raha hoon.