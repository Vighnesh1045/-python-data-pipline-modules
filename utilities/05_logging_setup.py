"""
Sets up basicConfig logging with the 5 standard severity levels, writing
formatted log lines to a file instead of just printing to the console.
"""
import logging

# ===== SETUP: configure the logger (this happens once, at the top) =====
logging.basicConfig(
    level=logging.INFO,     # only messages at this severity or above get shown
    format='%(asctime)s - %(levelname)s - %(message)s',   # what the output looks like
    filename='app.log',     # also saved to a FILE (print() doesn't do that)
    filemode='w'
)
logger = logging.getLogger("MyScript")

# ===== 5 SEVERITY LEVELS - from least to most serious =====
logger.debug("Only needed while debugging - hidden by default")
logger.info("Normal operation - e.g. 'Sales Orders fetched successfully'")
logger.warning("Something odd but not a crash - e.g. 'price was missing, used a default'")
logger.error("Something failed - e.g. 'ERP update failed for this order'")
logger.critical("Very serious - e.g. 'the entire pipeline crashed'")

print("Logging done - now let's look at 'app.log':")
