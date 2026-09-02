# cat << 'EOF' > /home/claude/pandas_merge_fallback.py
import pandas as pd

sales_orders = pd.DataFrame({
    'item_code': ['MACHINE-A', 'SPARE-X', 'ACC-Y', 'MACHINE-C'],
    'so_name': ['SO-001', 'SO-002', 'SO-003', 'SO-004'],
    'qty': [1, 5, 3, 1]
})

# Teen alag price lists - jaise tumhare script mein hai
machine_prices = pd.DataFrame({'item_code': ['MACHINE-A', 'MACHINE-C'], 'rate': [100000, 80000]})
standard_prices = pd.DataFrame({'item_code': ['SPARE-X'], 'rate': [500]})
accessory_prices = pd.DataFrame({'item_code': ['ACC-Y'], 'rate': [1200]})

# ===== STEP 1: Pehle Standard price list se try karo (merge + rename) =====
result = sales_orders.merge(standard_prices, on='item_code', how='left')
result = result.rename(columns={'rate': 'final_rate'})
print("Step 1 (Standard list se merge):\n", result, "\n")

# ===== STEP 2: Jahan STILL NaN hai (match nahi mila), Accessory list try karo =====
missing_mask = result['final_rate'].isna()   # True/False Series - kahan NaN hai
print("Kahan-kahan price abhi bhi missing hai:\n", missing_mask, "\n")

# Sirf un missing rows ko accessory_prices se merge karo
result_missing = result[missing_mask].drop(columns='final_rate').merge(
    accessory_prices, on='item_code', how='left'
).rename(columns={'rate': 'final_rate'})

# Wapas combine karo - jo pehle mile the + jo ab accessory se mile
result_found = result[~missing_mask]   # ~ = NOT, matlab jo NaN NAHI tha
result = pd.concat([result_found, result_missing])
print("Step 2 ke baad (Accessory list se fallback):\n", result, "\n")

# ===== STEP 3: Jo AB BHI missing hai, Machine list try karo (final fallback) =====
missing_mask = result['final_rate'].isna()
result_missing = result[missing_mask].drop(columns='final_rate').merge(
    machine_prices, on='item_code', how='left'
).rename(columns={'rate': 'final_rate'})
result_found = result[~missing_mask]
result = pd.concat([result_found, result_missing]).sort_values('so_name').reset_index(drop=True)

print("FINAL Result (teen-level fallback ke baad):\n", result)
# EOF
# python3 /home/claude/pandas_merge_fallback.py
# Output

# Step 1 (Standard list se merge):
#     item_code so_name  qty  final_rate
# 0  MACHINE-A  SO-001    1         NaN
# 1    SPARE-X  SO-002    5       500.0
# 2      ACC-Y  SO-003    3         NaN
# 3  MACHINE-C  SO-004    1         NaN 

# Kahan-kahan price abhi bhi missing hai:
#  0     True
# 1    False
# 2     True
# 3     True
# Name: final_rate, dtype: bool 

# Step 2 ke baad (Accessory list se fallback):
#     item_code so_name  qty  final_rate
# 1    SPARE-X  SO-002    5       500.0
# 0  MACHINE-A  SO-001    1         NaN
# 1      ACC-Y  SO-003    3      1200.0
# 2  MACHINE-C  SO-004    1         NaN 

# FINAL Result (teen-level fallback ke baad):
#     item_code so_name  qty  final_rate
# 0  MACHINE-A  SO-001    1    100000.0
# 1    SPARE-X  SO-002    5       500.0
# 2      ACC-Y  SO-003    3      1200.0
# 3  MACHINE-C  SO-004    1     80000.0