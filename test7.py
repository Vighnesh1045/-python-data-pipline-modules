# cat << 'EOF' > /home/claude/os_example.py
import os

# ===== 1. os.path.join - OS ke hisaab se sahi separator use karta hai =====
folder = "reports"
filename = "sales_data.xlsx"
full_path = os.path.join(folder, filename)
print("Joined path:", full_path)   # Linux pe 'reports/sales_data.xlsx', Windows pe 'reports\\sales_data.xlsx'

# ===== 2. os.path.dirname(__file__) - is script ka folder path nikaalna =====
# __file__ = "is Python file ka path jahan yeh code likha hai"
print("\nCurrent script ka folder:", os.path.dirname(os.path.abspath(__file__)))

# ===== 3. os.path.exists - file/folder hai ya nahi, check karna =====
print("\nKya 'reports' folder exist karta hai?", os.path.exists("reports"))

# ===== 4. os.makedirs - folder banao agar exist nahi karta =====
if not os.path.exists("reports"):
    os.makedirs("reports")
    print("'reports' folder ban gaya!")
else:
    print("'reports' folder pehle se hai")

# ===== 5. os.environ - environment variables padhna =====
# Yeh system-level settings hoti hain, jaise 'DISPLAY' (Linux GUI hai ya nahi, yeh batata hai)
print("\nHOME environment variable:", os.environ.get('HOME', 'Not set'))
print("Kya DISPLAY set hai (GUI available)?", 'DISPLAY' in os.environ)
# EOF
# cd /home/claude && python3 os_example.py
# Output

# Joined path: reports/sales_data.xlsx

# Current script ka folder: /home/claude

# Kya 'reports' folder exist karta hai? False
# 'reports' folder ban gaya!

# HOME environment variable: /root
# Kya DISPLAY set hai (GUI available)? False