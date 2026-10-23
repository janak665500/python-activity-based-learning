# Case Study 61: Nested List Examination Seating Validation
# Allowed Concepts: Variables, Data Types, Operators, Conditionals, Loops, Strings, Lists, Tuples & Unpacking
# Prohibited: Functions, Classes/OOP, Dictionaries, Sets, External Libraries

print("=" * 75)
print("     EXAMINATION SEATING MATRIX INTEGRITY AUDITOR (Case Study 61)")
print("=" * 75)

mode_input = input("Enter '1' for interactive entry or '0' for Automated Test Dataset: ").strip()

# Seating grid represented as a 2D nested list (Rows x Columns)
hall_grid = []
reserved_coords = []

if mode_input == "" or mode_input == "0" or mode_input.lower() == "demo":
    print("\n[Loading Benchmark Audit Hall Layout: 4 Rows x 5 Columns with Injected Test Anomalies]")
    rows = 4
    cols = 5
    
    # Official reserved/damaged coordinates list: (row, col)
    reserved_coords.append((1, 1))
    reserved_coords.append((2, 3))
    
    # 2D Grid with intentional test violations:
    # - Duplicate student "CS102" seated at (0, 2) and (3, 1)
    # - Unauthorized student "EC205" seated in reserved desk (1, 1)
    # - Branch adjacency violation at (0, 0) "CS101" and (0, 1) "CS104"
    hall_grid.append(["CS101", "CS104", "CS102", "EC201", "CS103"])
    hall_grid.append(["EC202", "EC205", "CS105", "EC203", "CS106"])
    hall_grid.append(["CS107", "EC204", "CS108", "[RESERVED]", "EC206"])
    hall_grid.append(["EC207", "CS102", "[EMPTY]", "EC208", "[EMPTY]"])
else:
    rows = int(input("Enter number of Rows in Examination Hall: ").strip())
    cols = int(input("Enter number of Columns in Examination Hall: ").strip())
    
    num_res = int(input("Enter number of officially designated reserved desks: ").strip())
    for i in range(num_res):
        rr = int(input(f"  Reserved desk #{i+1} row: ").strip())
        rc = int(input(f"  Reserved desk #{i+1} col: ").strip())
        reserved_coords.append((rr, rc))
        
    print("\nEnter seating matrix row by row (space-separated tokens or roll numbers):")
    for r in range(rows):
        line = input(f"  Row {r} ({cols} values): ").strip().split()
        while len(line) < cols:
            line.append("[EMPTY]")
        hall_grid.append(line[:cols])

print("\n" + "-" * 75)
print("STAGE 1: VISUALIZING INPUT SEATING PLAN MATRIX")
print("-" * 75)

header_str = "       "
for c in range(cols):
    header_str = header_str + f"Col {c:<8} "
print(header_str)
print("       " + "-" * (cols * 12))

for r in range(rows):
    row_str = f"Row {r:<2} | "
    for c in range(cols):
        cell_val = hall_grid[r][c]
        row_str = row_str + f"{cell_val:<11} "
    print(row_str)

# ---------------------------------------------------------
# STAGE 2: MULTI-FACETED SEATING AUDIT EXECUTION
# ---------------------------------------------------------
# Audit tracking lists (no dictionaries, no sets):
seen_students = []     # List of student IDs encountered
seen_positions = []    # Parallel list of coordinate tuples
duplicate_errors = []  # List of tuples: (student_id, (r1, c1), (r2, c2))

reserved_violations = [] # List of tuples: (r, c, placed_student)
adjacency_violations = [] # List of tuples: (r1, c1, id1, r2, c2, id2, direction)

occupied_count = 0
empty_count = 0
official_reserved_count = len(reserved_coords)

for r in range(rows):
    for c in range(cols):
        val = hall_grid[r][c].strip()
        
        # Check if cell is an empty indicator
        if val == "[EMPTY]" or val == "EMPTY" or val == "---":
            empty_count = empty_count + 1
            continue
            
        # Check if cell is an acknowledged reserved placeholder
        if val == "[RESERVED]" or val == "RESERVED" or val == "[BLOCKED]":
            continue
            
        # Valid student detected
        occupied_count = occupied_count + 1
        
        # Check 1: Reserved Desk Violation
        for res_tuple in reserved_coords:
            (rr, rc) = res_tuple
            if r == rr and c == rc:
                reserved_violations.append((r, c, val))
                
        # Check 2: Duplicate Roll Number Audit (Linear search without sets)
        is_dup = False
        first_pos = (-1, -1)
        for s_idx in range(len(seen_students)):
            if seen_students[s_idx] == val:
                is_dup = True
                first_pos = seen_positions[s_idx]
                break
                
        if is_dup:
            duplicate_errors.append((val, first_pos, (r, c)))
        else:
            seen_students.append(val)
            seen_positions.append((r, c))

# Check 3: Anti-Cheating Adjacent Branch Audit
# Check right neighbor and bottom neighbor for each cell
for r in range(rows):
    for c in range(cols):
        current_val = hall_grid[r][c].strip()
        if current_val.startswith("[") or current_val == "---":
            continue
            
        current_branch = current_val[:2]
        
        # Horizontal Neighbor (Right)
        if c + 1 < cols:
            right_val = hall_grid[r][c + 1].strip()
            if not right_val.startswith("[") and right_val != "---":
                if current_branch == right_val[:2]:
                    adjacency_violations.append((r, c, current_val, r, c + 1, right_val, "Horizontal"))
                    
        # Vertical Neighbor (Down)
        if r + 1 < rows:
            down_val = hall_grid[r + 1][c].strip()
            if not down_val.startswith("[") and down_val != "---":
                if current_branch == down_val[:2]:
                    adjacency_violations.append((r, c, current_val, r + 1, c, down_val, "Vertical"))

# ---------------------------------------------------------
# STAGE 3: COMPREHENSIVE AUDIT REPORT GENERATION
# ---------------------------------------------------------
print("\n" + "=" * 75)
print("STAGE 2: DETAILED ANOMALY & MALPRACTICE AUDIT FINDINGS")
print("=" * 75)

total_errors = len(duplicate_errors) + len(reserved_violations) + len(adjacency_violations)

if len(duplicate_errors) > 0:
    print(f"\n[ALERT: DUPLICATE ALLOCATIONS DETECTED ({len(duplicate_errors)})]")
    for dup in duplicate_errors:
        (s_id, pos1, pos2) = dup
        print(f"  - Roll No '{s_id}' allocated multiple times: Seat {pos1} and Seat {pos2}")
else:
    print("\n[OK] No duplicate student allocations found.")

if len(reserved_violations) > 0:
    print(f"\n[ALERT: RESERVED/DAMAGED DESK VIOLATIONS ({len(reserved_violations)})]")
    for res_v in reserved_violations:
        (r, c, s_id) = res_v
        print(f"  - Unauthorized student '{s_id}' placed on reserved/damaged desk at Row {r}, Col {c}")
else:
    print("\n[OK] All reserved/damaged desks respected.")

if len(adjacency_violations) > 0:
    print(f"\n[ALERT: BRANCH ADJACENCY (MALPRACTICE RISK) VIOLATIONS ({len(adjacency_violations)})]")
    for adj in adjacency_violations:
        (r1, c1, id1, r2, c2, id2, direction) = adj
        print(f"  - {direction} Adjacency: '{id1}' at ({r1},{c1}) next to '{id2}' at ({r2},{c2}) [Both Branch '{id1[:2]}']")
else:
    print("\n[OK] Anti-cheating alternating branch constraint fully satisfied.")

print("\n" + "=" * 75)
print("STAGE 3: FINAL EXAMINATION HALL AUDIT VERDICT")
print("=" * 75)
print(f"Hall Dimensions        : {rows} Rows x {cols} Columns (Capacity: {rows * cols})")
print(f"Total Occupied Desks   : {occupied_count}")
print(f"Total Empty Desks      : {empty_count}")
print(f"Official Reserved Desks: {official_reserved_count}")
print(f"Total Discrepancies    : {total_errors}")

if total_errors == 0:
    print("\nAUDIT VERDICT: [PASSED - EXAMINATION SEATING PLAN APPROVED FOR USE]")
else:
    print(f"\nAUDIT VERDICT: [FAILED - {total_errors} CRITICAL ISSUES REQUIRE IMMEDIATE REMEDIATION]")
print("=" * 75)
