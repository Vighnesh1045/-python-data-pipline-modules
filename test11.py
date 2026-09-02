# cat << 'EOF' > /home/claude/pandas_merge.py
import pandas as pd

# ===== Table 1: Sales Order items =====
sales_orders = pd.DataFrame({
    'item_code': ['MACHINE-A', 'MACHINE-B', 'SPARE-X', 'MACHINE-C'],
    'so_name': ['SO-001', 'SO-002', 'SO-003', 'SO-004'],
    'qty': [1, 2, 5, 1]
})

# ===== Table 2: Price List =====
price_list = pd.DataFrame({
    'item_code': ['MACHINE-A', 'MACHINE-B', 'SPARE-X'],   # dhyaan do - MACHINE-C yahan MISSING hai!
    'price_list_rate': [100000, 250000, 500]
})


print("Sales Orders:\n", sales_orders, "\n")
print("Price List:\n", price_list, "\n")

# ===== merge() - dono ko 'item_code' ke base pe jodo =====
# how='left' matlab: LEFT table (sales_orders) ke saare rows RAKHO,
# chahe price_list mein match mile ya na mile
merged = sales_orders.merge(price_list, on='item_code', how='left')
print("Merged Result (how='left'):\n", merged)
# EOF
# python3 /home/claude/pandas_merge.py
# Output

# Sales Orders:
#     item_code so_name  qty
# 0  MACHINE-A  SO-001    1
# 1  MACHINE-B  SO-002    2
# 2    SPARE-X  SO-003    5
# 3  MACHINE-C  SO-004    1 

# Price List:
#     item_code  price_list_rate
# 0  MACHINE-A           100000
# 1  MACHINE-B           250000
# 2    SPARE-X              500 

# Merged Result (how='left'):
#     item_code so_name  qty  price_list_rate
# 0  MACHINE-A  SO-001    1         100000.0
# 1  MACHINE-B  SO-002    2         250000.0
# 2    SPARE-X  SO-003    5            500.0
# 3  MACHINE-C  SO-004    1              NaN