# cat << 'EOF' > /home/claude/pandas_groupby.py
import pandas as pd

# Item-level data - ek Sales Order mein multiple items ho sakte hain
items = pd.DataFrame({
    'so_name': ['SO-001', 'SO-001', 'SO-002', 'SO-002', 'SO-002', 'SO-003'],
    'item_code': ['MACHINE-A', 'SPARE-X', 'MACHINE-B', 'SPARE-X', 'ACC-Y', 'MACHINE-C'],
    'amount': [100000, 2500, 250000, 1000, 3600, 80000],
    'target': [80000, 2000, 200000, 800, 3000, 64000]
})
print("Item-level data:\n", items, "\n")

# ===== groupby - SO_NAME ke hisaab se GROUP karo, phir amount/target ka SUM lo =====
so_level = items.groupby('so_name')[['amount', 'target']].sum().reset_index()
print("SO-level aggregated data:\n", so_level, "\n")

# reset_index() kyun zaroori hai? Dekho iske bina kya hota:
so_level_without_reset = items.groupby('so_name')[['amount', 'target']].sum()
print("Bina reset_index() ke (so_name INDEX ban jaata hai, column nahi):\n", so_level_without_reset)
# EOF
# python3 /home/claude/pandas_groupby.py
# Output

# Item-level data:
#    so_name  item_code  amount  target
# 0  SO-001  MACHINE-A  100000   80000
# 1  SO-001    SPARE-X    2500    2000
# 2  SO-002  MACHINE-B  250000  200000
# 3  SO-002    SPARE-X    1000     800
# 4  SO-002      ACC-Y    3600    3000
# 5  SO-003  MACHINE-C   80000   64000 

# SO-level aggregated data:
#    so_name  amount  target
# 0  SO-001  102500   82000
# 1  SO-002  254600  203800
# 2  SO-003   80000   64000 

# Bina reset_index() ke (so_name INDEX ban jaata hai, column nahi):
#           amount  target
# so_name                
# SO-001   102500   82000
# SO-002   254600  203800
# SO-003    80000   64000