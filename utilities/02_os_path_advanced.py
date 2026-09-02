"""
More os.path utilities: basename, dirname, splitext, abspath, isfile/isdir,
and a real-world pattern for generating a timestamped report filename.
"""
import os
from datetime import datetime

full_path = "/C:/Users/dataanalysts/Desktop/Vighnesh/Learnings/Threading/test8.py"

# 1. basename - get just the FILENAME, drop the folder path
print("basename:", os.path.basename(full_path))

# 2. dirname - get just the FOLDER path, drop the filename
print("dirname:", os.path.dirname(full_path))

# 3. os.path is a MODULE, not a function - use os.path.abspath(), not os.path()
print("full path (abspath):", os.path.abspath(full_path))

# 4. splitext - split filename and EXTENSION apart
name_part, extension = os.path.splitext(full_path)
print("name part:", name_part)
print("extension:", extension)
# Useful when you want to save the same filename under a different extension

# 5. abspath - convert a RELATIVE path into a FULL/ABSOLUTE path
relative = "Threading/test8.py"
print("\nRelative:", relative)
print("Absolute:", os.path.abspath(relative))

# 6. isfile vs isdir - check whether something is a FILE or a FOLDER
print("\nIs this a file?", os.path.isfile(__file__))
print("Is this a folder?", os.path.isdir(os.path.dirname(__file__)))

# 7. REAL-WORLD PATTERN: dynamic filename with timestamp
# Same pattern used for report exports - build the filename from a base
# name plus a timestamp so re-runs don't overwrite older reports.
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
dynamic_filename = f"report_{timestamp}.xlsx"
dynamic_path = os.path.join("reports", dynamic_filename)
print("\nDynamic filename generated:", dynamic_path)
