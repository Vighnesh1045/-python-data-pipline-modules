# cat << 'EOF' > /home/claude/os_path_extra.py
import os
from datetime import datetime

full_path = "/C:/Users/dataanalysts/Desktop/Vighnesh/Learnings/Threading/test8.py"

# ===== 1. basename - sirf FILENAME nikaalo, folder path hata do =====
print("basename:", os.path.basename(full_path))
# Output: Realization_Report_2026-08-31.xlsx

# ===== 2. dirname - sirf FOLDER path nikaalo, filename hata do =====
print("dirname:", os.path.dirname(full_path))
# Output: /home/claude/reports

print("fullpath:", os.path(full_path))

# ===== 3. splitext - filename aur EXTENSION alag karo =====
name_part, extension = os.path.splitext(full_path)
print("name part:", name_part)
print("extension:", extension)
# Useful jab tum same filename ko different extension se save karna chahte ho

# ===== 4. abspath - RELATIVE path ko FULL/ABSOLUTE path mein convert karo =====
relative = "Threading/test8.py"
print("\nRelative:", relative)
print("Absolute:", os.path.abspath(relative))

# ===== 5. isfile vs isdir - check karo yeh FILE hai ya FOLDER =====
print("\nKya yeh ek file hai?", os.path.isfile(__file__))
print("Kya yeh ek folder hai?", os.path.isdir(os.path.dirname(__file__)))

# ===== 6. REAL-WORLD PATTERN: dynamic filename with timestamp =====
# Yeh tumhare script jaisa pattern hai - report ka naam timestamp ke saath banana
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
dynamic_filename = f"test8{timestamp}.py"
dynamic_path = os.path.join("Threadng", dynamic_filename)
print("\nDynamic filename generated:", dynamic_path)
# EOF
# python3 /home/claude/os_path_extra.py
# Output

# basename: Realization_Report_2026-08-31.xlsx
# dirname: /home/claude/reports
# name part: /home/claude/reports/Realization_Report_2026-08-31
# extension: .xlsx

# Relative: reports/data.xlsx
# Absolute: /reports/data.xlsx

# Kya yeh ek file hai? True
# Kya yeh ek folder hai? True

# Dynamic filename generated: reports/Realization_Report_2026-08-31_11-41.xlsx