"""
Demonstrates pandas merge(): joining two DataFrames on a shared key
column with a LEFT join, so unmatched rows are kept with NaN values.
"""
import pandas as pd

# ===== Table 1: Sales Order items =====
sales_orders = pd.DataFrame({
    'item_code': ['MACHINE-A', 'MACHINE-B', 'SPARE-X', 'MACHINE-C'],
    'so_name': ['SO-001', 'SO-002', 'SO-003', 'SO-004'],
    'qty': [1, 2, 5, 1]
})

# ===== Table 2: Price List =====
price_list = pd.DataFrame({
    'item_code': ['MACHINE-A', 'MACHINE-B', 'SPARE-X'],   # note - MACHINE-C is MISSING here!
    'price_list_rate': [100000, 250000, 500]
})


print("Sales Orders:\n", sales_orders, "\n")
print("Price List:\n", price_list, "\n")

# ===== merge() - join both on 'item_code' =====
# how='left' means: KEEP every row from the LEFT table (sales_orders),
# whether or not it finds a match in price_list
merged = sales_orders.merge(price_list, on='item_code', how='left')
print("Merged Result (how='left'):\n", merged)
