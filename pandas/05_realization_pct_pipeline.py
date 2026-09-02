"""
Flagship walkthrough: takes raw Sales Order line items through a full
reconciliation pipeline - multi-tier fallback pricing, MRP-tiered
targets, SO-level aggregation, and a Realization % formula (accounting
for commission, freight, and payment terms) with a final status
assignment. Mirrors the real Sales Order Realization % investigation
from the Electrolab Data Analyst Apprentice role.
"""
import pandas as pd

print("="*70)
print("STEP 1: RAW Sales Order line items (as fetched from the ERP)")
print("="*70)
so_items = pd.DataFrame({
    'sales_order': ['SO-001', 'SO-001', 'SO-002', 'SO-002', 'SO-003'],
    'item_code':   ['MACHINE-A', 'SPARE-X', 'MACHINE-B', 'ACC-Y', 'MACHINE-C'],
    'qty':         [1, 5, 1, 3, 1],
    'amount':      [95000, 2400, 240000, 3300, 78000],   # actual invoiced amount
})
print(so_items, "\n")

print("="*70)
print("STEP 2: Three price lists (Machine / Standard / Accessory)")
print("="*70)
machine_prices  = pd.DataFrame({'item_code': ['MACHINE-A', 'MACHINE-B', 'MACHINE-C'], 'mrp': [120000, 250000, 149000]})
standard_prices = pd.DataFrame({'item_code': ['SPARE-X'], 'rate': [500]})
accessory_prices= pd.DataFrame({'item_code': ['ACC-Y'], 'rate': [1200]})
print("Machine:\n", machine_prices, "\nStandard:\n", standard_prices, "\nAccessory:\n", accessory_prices, "\n")

print("="*70)
print("STEP 3: FALLBACK PRICING (merge + isna() + concat) - resolving price_list_rate")
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
print("STEP 4: TARGET calculation (MRP-tiered % rule via .apply())")
print("="*70)
def target_pct_rule(row):
    return 0.80 if row['price_list_rate'] < 150000 else 0.70
merged['target_pct'] = merged.apply(target_pct_rule, axis=1)
merged['target'] = merged['price_list_rate'] * merged['qty'] * merged['target_pct']
print(merged[['sales_order','item_code','price_list_rate','qty','target_pct','target']], "\n")

print("="*70)
print("STEP 5: SO-LEVEL AGGREGATION (groupby + sum)")
print("="*70)
so_level = merged.groupby('sales_order')[['amount', 'target']].sum().reset_index()
print(so_level, "\n")

print("="*70)
print("STEP 6: REALIZATION % FORMULA")
print("="*70)
# assume commission=2%, plus freight and payment_terms per SO
so_level['commission_rate'] = [2, 2, 2]
so_level['freight_amt'] = [500, 800, 200]
so_level['payment_terms_pct'] = [100, 50, 100]   # SO-002 only received 50% advance

so_level['realization_value'] = (
    (so_level['amount'] * (1 - so_level['commission_rate']/100) - so_level['freight_amt'])
    * (so_level['payment_terms_pct'] / 100)
)
so_level['realization_pct'] = ((so_level['realization_value'] / so_level['target']) * 100).round(1)
print(so_level[['sales_order','amount','target','realization_value','realization_pct']], "\n")

print("="*70)
print("STEP 7: STATUS ASSIGNMENT (business rule via .apply())")
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
