# Case Study 88: Multi-Branch Retail Inventory Transfer
# Allowed Concepts: Variables, Data Types, Operators, Conditionals, Loops, Strings, Lists, Tuples & Unpacking
# Prohibited: Functions, Classes/OOP, Dictionaries, External Libraries (numpy, pandas, scipy)

print("=" * 80)
print("     MULTI-BRANCH RETAIL INVENTORY RECONCILIATION & TRANSFER (Case Study 88)")
print("=" * 80)

mode_input = input("Enter '1' for interactive entry or '0' for Automated Test Dataset: ").strip()

branches = ["Campus-North", "Campus-South", "Campus-Central", "Campus-East"]
products = ["Python Textbook", "Lab Notebook", "Scientific Calc", "Engg Drawing Kit"]

num_branches = len(branches)
num_products = len(products)

# 2D Matrices: current_stock[branch_idx][product_idx]
current_stock = []
target_stock = []

if mode_input == "" or mode_input == "0" or mode_input.lower() == "demo":
    print("\n[Loading Standard Retail Logistics Network: 4 Branches x 4 Key Academic Items...]")
    # Current Stock levels (Rows: Branches, Cols: Products)
    current_stock.append([45, 120, 15, 8])   # North: Surplus in Textbooks, Deficit in Calculators & Kits
    current_stock.append([10, 80, 50, 40])   # South: Deficit in Textbooks, Large Surplus in Calculators & Kits
    current_stock.append([25, 200, 30, 25])  # Central: Huge Notebook surplus, balanced elsewhere
    current_stock.append([12, 60, 10, 12])   # East: Deficits across multiple products

    # Target Requirement levels (Rows: Branches, Cols: Products)
    target_stock.append([20, 100, 30, 20])   # North targets
    target_stock.append([30, 100, 25, 20])   # South targets
    target_stock.append([25, 120, 25, 25])   # Central targets
    target_stock.append([25, 100, 20, 20])   # East targets
else:
    print("\nEntering Custom Inventory Parameters...")
    for b_i in range(num_branches):
        print(f"\nBranch: {branches[b_i]}")
        cur_row = []
        tar_row = []
        for p_j in range(num_products):
            c_val = int(input(f"  Current stock of {products[p_j]}: ").strip())
            t_val = int(input(f"  Target requirement of {products[p_j]}: ").strip())
            cur_row.append(c_val)
            tar_row.append(t_val)
        current_stock.append(cur_row)
        target_stock.append(tar_row)

# ---------------------------------------------------------
# STAGE 1: VARIANCE & RECONCILIATION MATRIX GENERATION
# ---------------------------------------------------------
# Net variance matrix = current_stock - target_stock
# Positive (+) indicates SURPLUS; Negative (-) indicates DEFICIT; 0 is BALANCED
variance_matrix = []
for b_i in range(num_branches):
    var_row = []
    for p_j in range(num_products):
        diff = current_stock[b_i][p_j] - target_stock[b_i][p_j]
        var_row.append(diff)
    variance_matrix.append(var_row)

print("\n" + "-" * 80)
print("STAGE 1: PRE-TRANSFER INVENTORY VARIANCE STATUS")
print("-" * 80)
header_str = f"{'Branch Name':<16} "
for p in products:
    header_str = header_str + f"{p[:13]:<15} "
print(header_str)
print("-" * 80)

for b_i in range(num_branches):
    row_str = f"{branches[b_i]:<16} "
    for p_j in range(num_products):
        var_val = variance_matrix[b_i][p_j]
        if var_val > 0:
            status_tag = f"+{var_val} (Surplus)"
        elif var_val < 0:
            status_tag = f"{var_val} (Deficit)"
        else:
            status_tag = "0 (Balanced)"
        row_str = row_str + f"{status_tag:<15} "
    print(row_str)

# ---------------------------------------------------------
# STAGE 2: GREEDY INTER-BRANCH TRANSFER OPTIMIZATION
# ---------------------------------------------------------
# Directives list stores: (product_name, from_branch, to_branch, units, cost)
transfer_directives = []
UNIT_SHIPPING_COST = 8.50 # Standard inter-campus transfer fee per unit (Rs.)

# Work on a copy of current_stock to simulate dynamic movements
working_stock = []
for r in range(num_branches):
    w_row = []
    for c in range(num_products):
        w_row.append(current_stock[r][c])
    working_stock.append(w_row)

# Transfer logic executed product by product
for p_j in range(num_products):
    p_name = products[p_j]
    
    # Outer loop continues while transfers can be made for this product
    transfers_possible = True
    while transfers_possible:
        # Find first surplus branch and first deficit branch for product p_j
        surplus_branch_idx = -1
        deficit_branch_idx = -1
        
        for b_i in range(num_branches):
            net_diff = working_stock[b_i][p_j] - target_stock[b_i][p_j]
            if net_diff > 0 and surplus_branch_idx == -1:
                surplus_branch_idx = b_i
            elif net_diff < 0 and deficit_branch_idx == -1:
                deficit_branch_idx = b_i
                
        # If both a donor (surplus) and receiver (deficit) exist, execute transfer
        if surplus_branch_idx != -1 and deficit_branch_idx != -1:
            avail_surplus = working_stock[surplus_branch_idx][p_j] - target_stock[surplus_branch_idx][p_j]
            needed_deficit = target_stock[deficit_branch_idx][p_j] - working_stock[deficit_branch_idx][p_j]
            
            # Transfer amount is the minimum of what is available and what is needed
            transfer_qty = avail_surplus if avail_surplus < needed_deficit else needed_deficit
            
            # Apply stock transfer
            working_stock[surplus_branch_idx][p_j] = working_stock[surplus_branch_idx][p_j] - transfer_qty
            working_stock[deficit_branch_idx][p_j] = working_stock[deficit_branch_idx][p_j] + transfer_qty
            
            shipping_fee = round(transfer_qty * UNIT_SHIPPING_COST, 2)
            transfer_directives.append((p_name, branches[surplus_branch_idx], branches[deficit_branch_idx], transfer_qty, shipping_fee))
        else:
            transfers_possible = False

# ---------------------------------------------------------
# STAGE 3: TRANSFER DIRECTIVES & FINAL AUDIT
# ---------------------------------------------------------
print("\n" + "=" * 80)
print("STAGE 2: RECOMMENDED INTER-BRANCH STOCK TRANSFER MANIFEST")
print("=" * 80)
print(f"{'Product':<18} {'From (Donor)':<16} {'To (Recipient)':<16} {'Units':<8} {'Logistics Cost'}")
print("-" * 80)

total_units_moved = 0
total_logistics_cost = 0.0

for t in transfer_directives:
    (p_nm, src, dst, qty, fee) = t
    total_units_moved = total_units_moved + qty
    total_logistics_cost = total_logistics_cost + fee
    print(f"{p_nm:<18} {src:<16} {dst:<16} {qty:<8} Rs. {fee:<10.2f}")

if len(transfer_directives) == 0:
    print("  No internal transfers possible or required.")

print("-" * 80)
print(f"Total Transfer Actions: {len(transfer_directives)} | Total Units Relocated: {total_units_moved} | Total Cost: Rs. {total_logistics_cost:.2f}")

# ---------------------------------------------------------
# STAGE 4: POST-TRANSFER INVENTORY & EXTERNAL PROCUREMENT AUDIT
# ---------------------------------------------------------
print("\n" + "=" * 80)
print("STAGE 3: POST-TRANSFER RECONCILED INVENTORY STATUS")
print("=" * 80)
header_str = f"{'Branch Name':<16} "
for p in products:
    header_str = header_str + f"{p[:13]:<15} "
print(header_str)
print("-" * 80)

external_procurement_needed = []

for b_i in range(num_branches):
    row_str = f"{branches[b_i]:<16} "
    for p_j in range(num_products):
        final_stock = working_stock[b_i][p_j]
        req_target = target_stock[b_i][p_j]
        gap = final_stock - req_target
        if gap < 0:
            status_tag = f"{final_stock} [SHORT {-gap}]"
            external_procurement_needed.append((branches[b_i], products[p_j], -gap))
        elif gap > 0:
            status_tag = f"{final_stock} [SURPLUS +{gap}]"
        else:
            status_tag = f"{final_stock} [SATISFIED]"
        row_str = row_str + f"{status_tag:<15} "
    print(row_str)

print("\n" + "=" * 80)
print("STAGE 4: EXTERNAL WAREHOUSE RE-ORDER ORDERS REQUIRED")
print("=" * 80)
if len(external_procurement_needed) > 0:
    print("Internal inter-branch inventory was insufficient for the following remaining deficits:")
    for ext in external_procurement_needed:
        (b_nm, p_nm, deficit_qty) = ext
        print(f"  [RE-ORDER] {b_nm:<16} requires {deficit_qty} additional units of '{p_nm}' from Central Vendor")
else:
    print("  [SUCCESS] 100% of branch deficits resolved purely through internal inter-branch rebalancing!")
print("=" * 80)
