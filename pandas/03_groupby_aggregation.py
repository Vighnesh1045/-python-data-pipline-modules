"""
Demonstrates pandas groupby(): rolling up item-level rows into
sales-order-level totals, and why reset_index() matters afterward.
"""
import pandas as pd

# Item-level data - a single Sales Order can have multiple items
items = pd.DataFrame({
    'so_name': ['SO-001', 'SO-001', 'SO-002', 'SO-002', 'SO-002', 'SO-003'],
    'item_code': ['MACHINE-A', 'SPARE-X', 'MACHINE-B', 'SPARE-X', 'ACC-Y', 'MACHINE-C'],
    'amount': [100000, 2500, 250000, 1000, 3600, 80000],
    'target': [80000, 2000, 200000, 800, 3000, 64000]
})
print("Item-level data:\n", items, "\n")

# ===== groupby - group by SO_NAME, then SUM the amount/target =====
so_level = items.groupby('so_name')[['amount', 'target']].sum().reset_index()
print("SO-level aggregated data:\n", so_level, "\n")

# Why is reset_index() needed? See what happens without it:
so_level_without_reset = items.groupby('so_name')[['amount', 'target']].sum()
print("Without reset_index() (so_name becomes the INDEX, not a column):\n", so_level_without_reset)
