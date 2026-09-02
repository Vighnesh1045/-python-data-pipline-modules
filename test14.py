# cat << 'EOF' > /home/claude/pandas_apply.py
import pandas as pd

machines = pd.DataFrame({
    'item_code': ['MACHINE-A', 'MACHINE-B', 'MACHINE-C'],
    'mrp': [120000, 250000, 149000]
})

# ===== Custom function likho jo EK ROW pe kaam kare =====
def calculate_target_percent(row):
    if row['mrp'] < 150000:
        return 0.80   # 80% target
    else:
        return 0.70   # 70% target

# ===== apply(func, axis=1) - axis=1 matlab "row-by-row chalao" (axis=0 hota column-wise) =====
machines['target_pct'] = machines.apply(calculate_target_percent, axis=1)
machines['target_amount'] = machines['mrp'] * machines['target_pct']

print(machines)
# EOF
# python3 /home/claude/pandas_apply.py
# Output

#    item_code     mrp  target_pct  target_amount
# 0  MACHINE-A  120000         0.8        96000.0
# 1  MACHINE-B  250000         0.7       175000.0
# 2  MACHINE-C  149000         0.8       119200.0