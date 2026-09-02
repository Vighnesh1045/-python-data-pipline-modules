"""
Demonstrates DataFrame.apply(axis=1): running a custom row-by-row
function to apply a business rule (an MRP-tiered target percentage).
"""
import pandas as pd

machines = pd.DataFrame({
    'item_code': ['MACHINE-A', 'MACHINE-B', 'MACHINE-C'],
    'mrp': [120000, 250000, 149000]
})


# ===== Write a custom function that works on ONE ROW =====
def calculate_target_percent(row):
    if row['mrp'] < 150000:
        return 0.80   # 80% target
    else:
        return 0.70   # 70% target


# ===== apply(func, axis=1) - axis=1 means "run row-by-row" (axis=0 is column-wise) =====
machines['target_pct'] = machines.apply(calculate_target_percent, axis=1)
machines['target_amount'] = machines['mrp'] * machines['target_pct']

print(machines)
