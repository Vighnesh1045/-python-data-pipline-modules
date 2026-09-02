# cat << 'EOF' > /home/claude/logging_example.py
import logging

# ===== SETUP: logger configure karo (yeh ek baar top pe hota hai) =====
logging.basicConfig(
    level=logging.INFO,     # kaunsi severity se upar ki cheezein dikhani hain
    format='%(asctime)s - %(levelname)s - %(message)s',   # kaisa dikhega output
    filename='app.log',     # FILE mein bhi save hoga (print() aisa nahi karta)
    filemode='w'
)
logger = logging.getLogger("MyScript")

# ===== 5 SEVERITY LEVELS - kam se zyada serious =====
logger.debug("Yeh sirf debugging ke waqt chahiye - normally hide rehta hai")
logger.info("Normal operation - jaise 'Sales Orders fetch ho gaye'")
logger.warning("Kuch ajeeb hai but crash nahi hua - jaise 'price missing tha, default use kiya'")
logger.error("Kuch fail hua - jaise 'ERP update fail ho gaya is order ke liye'")
logger.critical("Bahut serious - jaise 'poora pipeline hi crash ho gaya'")

print("Logging ho gayi - ab 'app.log' file dekhte hain:")
# EOF
# cd /home/claude && python3 logging_example.py
# echo "---"
# cat app.log
# Output

# Logging ho gayi - ab 'app.log' file dekhte hain:
# ---
# 2026-09-01 09:50:43,183 - INFO - Normal operation - jaise 'Sales Orders fetch ho gaye'
# 2026-09-01 09:50:43,183 - WARNING - Kuch ajeeb hai but crash nahi hua - jaise 'price missing tha, default use kiya'
# 2026-09-01 09:50:43,183 - ERROR - Kuch fail hua - jaise 'ERP update fail ho gaya is order ke liye'
# 2026-09-01 09:50:43,183 - CRITICAL - Bahut serious - jaise 'poora pipeline hi crash ho gaya'