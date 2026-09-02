# cat << 'EOF' > /home/claude/full_realization_walkthrough.py
import pandas as pd
import numpy as np

print("="*70)
print("STEP 1: RAW Sales Order line items (jaise ERP se fetch hua)")
print("="*70)
so_items = pd.DataFrame({
    'sales_order': ['SO-001', 'SO-001', 'SO-002', 'SO-002', 'SO-003'],
    'item_code':   ['MACHINE-A', 'SPARE-X', 'MACHINE-B', 'ACC-Y', 'MACHINE-C'],
    'qty':         [1, 5, 1, 3, 1],
    'amount':      [95000, 2400, 240000, 3300, 78000],   # actual invoiced amount
})
print(so_items, "\n")

print("="*70)
print("STEP 2: Teen price lists (Machine / Standard / Accessory)")
print("="*70)
machine_prices  = pd.DataFrame({'item_code': ['MACHINE-A', 'MACHINE-B', 'MACHINE-C'], 'mrp': [120000, 250000, 149000]})
standard_prices = pd.DataFrame({'item_code': ['SPARE-X'], 'rate': [500]})
accessory_prices= pd.DataFrame({'item_code': ['ACC-Y'], 'rate': [1200]})
print("Machine:\n", machine_prices, "\nStandard:\n", standard_prices, "\nAccessory:\n", accessory_prices, "\n")

print("="*70)
print("STEP 4: FALLBACK PRICING (merge + isna() + concat) - price_list_rate nikaalna")
print("="*70)
merged = so_items.merge(standard_prices, on='item_code', how='left').rename(columns={'rate': 'price_list_rate'})
missing = merged['price_list_rate'].isna()
found = merged[~missing]
retry = merged[missing].drop(columns='price_list_rate').merge(accessory_prices, on='item_code', how='left').rename(columns={'rate': 'price_list_rate'})
merged = pd.concat([found, retry])
missing = merged['price_list_rate'].isna()
found = merged[~missing]
retry = merged[missing].drop(columns='price_list_rate').merge(machine_prices, on='item_code', how='left').rename(columns={'mrp': 'price_list_rate'})
merged = pd.concat([found, retry]).sort_values(['sales_order','item_code']).reset_index(drop=True)
print(merged, "\n")

print("="*70)
print("STEP 6: TARGET calculation (MRP-tiered % rule via .apply())")
print("="*70)
def target_pct_rule(row):
    return 0.80 if row['price_list_rate'] < 150000 else 0.70
merged['target_pct'] = merged.apply(target_pct_rule, axis=1)
merged['target'] = merged['price_list_rate'] * merged['qty'] * merged['target_pct']
print(merged[['sales_order','item_code','price_list_rate','qty','target_pct','target']], "\n")

print("="*70)
print("STEP 7: SO-LEVEL AGGREGATION (groupby + sum)")
print("="*70)
so_level = merged.groupby('sales_order')[['amount', 'target']].sum().reset_index()
print(so_level, "\n")

print("="*70)
print("STEP 9: REALIZATION % FORMULA")
print("="*70)
# maan lo commission=2%, freight aur payment_terms bhi diye
so_level['commission_rate'] = [2, 2, 2]
so_level['freight_amt'] = [500, 800, 200]
so_level['payment_terms_pct'] = [100, 50, 100]   # SO-002 ka sirf 50% advance aaya

so_level['realization_value'] = (
    (so_level['amount'] * (1 - so_level['commission_rate']/100) - so_level['freight_amt'])
    * (so_level['payment_terms_pct'] / 100)
)
so_level['realization_pct'] = ((so_level['realization_value'] / so_level['target']) * 100).round(1)
print(so_level[['sales_order','amount','target','realization_value','realization_pct']], "\n")

print("="*70)
print("STEP 10: STATUS ASSIGNMENT (.apply() se business rule)")
print("="*70)
def assign_status(row):
    if row['realization_pct'] <= 0:
        return "Pending"
    elif row['realization_pct'] < 100:
        return "Partial"
    else:
        return "Complete"
so_level['status'] = so_level.apply(assign_status, axis=1)
print(so_level[['sales_order','realization_pct','status']])
# EOF
# python3 /home/claude/full_realization_walkthrough.py
# Output

# ======================================================================
# STEP 1: RAW Sales Order line items (jaise ERP se fetch hua)
# ======================================================================
#   sales_order  item_code  qty  amount
# 0      SO-001  MACHINE-A    1   95000
# 1      SO-001    SPARE-X    5    2400
# 2      SO-002  MACHINE-B    1  240000
# 3      SO-002      ACC-Y    3    3300
# 4      SO-003  MACHINE-C    1   78000 

# ======================================================================
# STEP 2: Teen price lists (Machine / Standard / Accessory)
# ======================================================================
# Machine:
#     item_code     mrp
# 0  MACHINE-A  120000
# 1  MACHINE-B  250000
# 2  MACHINE-C  149000 
# Standard:
#    item_code  rate
# 0   SPARE-X   500 
# Accessory:
#    item_code  rate
# 0     ACC-Y  1200 

# ======================================================================
# STEP 4: FALLBACK PRICING (merge + isna() + concat) - price_list_rate nikaalna
# ======================================================================
#   sales_order  item_code  qty  amount  price_list_rate
# 0      SO-001  MACHINE-A    1   95000         120000.0
# 1      SO-001    SPARE-X    5    2400            500.0
# 2      SO-002      ACC-Y    3    3300           1200.0
# 3      SO-002  MACHINE-B    1  240000         250000.0
# 4      SO-003  MACHINE-C    1   78000         149000.0 

# ======================================================================
# STEP 6: TARGET calculation (MRP-tiered % rule via .apply())
# ======================================================================
#   sales_order  item_code  price_list_rate  qty  target_pct    target
# 0      SO-001  MACHINE-A         120000.0    1         0.8   96000.0
# 1      SO-001    SPARE-X            500.0    5         0.8    2000.0
# 2      SO-002      ACC-Y           1200.0    3         0.8    2880.0
# 3      SO-002  MACHINE-B         250000.0    1         0.7  175000.0
# 4      SO-003  MACHINE-C         149000.0    1         0.8  119200.0 

# ======================================================================
# STEP 7: SO-LEVEL AGGREGATION (groupby + sum)
# ======================================================================
#   sales_order  amount    target
# 0      SO-001   97400   98000.0
# 1      SO-002  243300  177880.0
# 2      SO-003   78000  119200.0 

# ======================================================================
# STEP 9: REALIZATION % FORMULA
# ======================================================================
#   sales_order  amount    target  realization_value  realization_pct
# 0      SO-001   97400   98000.0            94952.0             96.9
# 1      SO-002  243300  177880.0           118817.0             66.8
# 2      SO-003   78000  119200.0            76240.0             64.0 

# ======================================================================
# STEP 10: STATUS ASSIGNMENT (.apply() se business rule)
# ======================================================================
#   sales_order  realization_pct   status
# 0      SO-001             96.9  Partial
# 1      SO-002             66.8  Partial
# 2      SO-003             64.0  Partial