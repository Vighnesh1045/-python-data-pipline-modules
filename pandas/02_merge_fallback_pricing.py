"""
Demonstrates a multi-tier merge fallback pattern: try one price list,
then for whatever's still missing try the next, and so on - a common
pattern when line items can come from several different price lists.
"""
import pandas as pd

sales_orders = pd.DataFrame({
    'item_code': ['MACHINE-A', 'SPARE-X', 'ACC-Y', 'MACHINE-C'],
    'so_name': ['SO-001', 'SO-002', 'SO-003', 'SO-004'],
    'qty': [1, 5, 3, 1]
})

# Three separate price lists - like in the real script
machine_prices = pd.DataFrame({'item_code': ['MACHINE-A', 'MACHINE-C'], 'rate': [100000, 80000]})
standard_prices = pd.DataFrame({'item_code': ['SPARE-X'], 'rate': [500]})
accessory_prices = pd.DataFrame({'item_code': ['ACC-Y'], 'rate': [1200]})

# ===== STEP 1: Try the Standard price list first (merge + rename) =====
result = sales_orders.merge(standard_prices, on='item_code', how='left')
result = result.rename(columns={'rate': 'final_rate'})
print("Step 1 (merged with Standard list):\n", result, "\n")

# ===== STEP 2: Wherever it's STILL NaN (no match), try the Accessory list =====
missing_mask = result['final_rate'].isna()   # True/False Series - where is it NaN
print("Where the price is still missing:\n", missing_mask, "\n")

# Merge only the missing rows against accessory_prices
result_missing = result[missing_mask].drop(columns='final_rate').merge(
    accessory_prices, on='item_code', how='left'
).rename(columns={'rate': 'final_rate'})

# Combine back together - what matched before + what matched via accessory
result_found = result[~missing_mask]   # ~ = NOT, i.e. rows that weren't NaN
result = pd.concat([result_found, result_missing])
print("After Step 2 (fallback to Accessory list):\n", result, "\n")

# ===== STEP 3: Whatever is STILL missing, try the Machine list (final fallback) =====
missing_mask = result['final_rate'].isna()
result_missing = result[missing_mask].drop(columns='final_rate').merge(
    machine_prices, on='item_code', how='left'
).rename(columns={'rate': 'final_rate'})
result_found = result[~missing_mask]
result = pd.concat([result_found, result_missing]).sort_values('so_name').reset_index(drop=True)

print("FINAL Result (after three-level fallback):\n", result)
