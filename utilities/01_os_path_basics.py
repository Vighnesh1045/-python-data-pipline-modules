"""
Basic os.path utilities: joining paths, finding a script's own folder,
checking whether a path exists, creating folders, and reading env vars.
"""
import os

# 1. os.path.join - uses the correct separator for the current OS
folder = "reports"
filename = "sales_data.xlsx"
full_path = os.path.join(folder, filename)
print("Joined path:", full_path)   # 'reports/sales_data.xlsx' on Linux, 'reports\\sales_data.xlsx' on Windows

# 2. os.path.dirname(__file__) - get this script's own folder path
# __file__ = "the path to this Python file"
print("\nThis script's folder:", os.path.dirname(os.path.abspath(__file__)))

# 3. os.path.exists - check whether a file/folder exists
print("\nDoes the 'reports' folder exist?", os.path.exists("reports"))

# 4. os.makedirs - create the folder if it doesn't exist
if not os.path.exists("reports"):
    os.makedirs("reports")
    print("'reports' folder created!")
else:
    print("'reports' folder already exists")

# 5. os.environ - read environment variables
# These are system-level settings, like 'DISPLAY' (tells you if a Linux GUI is available)
print("\nHOME environment variable:", os.environ.get('HOME', 'Not set'))
print("Is DISPLAY set (GUI available)?", 'DISPLAY' in os.environ)
