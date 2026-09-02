# cat << 'EOF' > /home/claude/atexit_crash_example.py
import atexit

def cleanup_function():
    print("🧹 Cleanup ho raha hai, chahe crash hua ho ya na hua ho!")

atexit.register(cleanup_function)

print("Program shuru hua...")
print("Ab jaan-boojh kar error create karta hoon...")

result = 10 / 0   # yeh crash karega (ZeroDivisionError)

print("Yeh line kabhi print nahi hogi")   # crash ki wajah se yahan tak pahunchega hi nahi
# EOF
# python3 /home/claude/atexit_crash_example.py
# echo "---exit code: $?---"
# Output

# Program shuru hua...
# Ab jaan-boojh kar error create karta hoon...
# 🧹 Cleanup ho raha hai, chahe crash hua ho ya na hua ho!
# ---exit code: 1---