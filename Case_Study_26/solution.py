# Case Study 26: Nested Loop Examination Seating Generator
# Allowed Concepts: Variables, Data Types, Operators, Conditionals, Loops, Strings, Lists, Tuples & Unpacking
# Prohibited: Functions, Classes/OOP, Dictionaries, External Libraries

print("=" * 70)
print("     EXAMINATION SEATING MATRIX GENERATOR (Case Study 26)")
print("=" * 70)

mode_input = input("Enter '1' for Interactive Input or '0' for Automated Test Dataset: ").strip()

if mode_input == "" or mode_input == "0" or mode_input.lower() == "demo":
    print("\n[Loading Standard Test Configuration: 5 Rows x 6 Columns (Capacity: 30)]")
    rows = 5
    cols = 6
    # 13 CSE students, 12 ECE students, plus reserved broken seats
    dept_a_name = "CSE"
    dept_b_name = "ECE"
    students_a = ["CS101", "CS102", "CS103", "CS104", "CS105", "CS106", "CS107", "CS108", "CS109", "CS110", "CS111", "CS112", "CS113"]
    students_b = ["EC201", "EC202", "EC203", "EC204", "EC205", "EC206", "EC207", "EC208", "EC209", "EC210", "EC211", "EC212"]
    # Broken/Reserved seat coordinates as tuples: (row_idx, col_idx)
    blocked_seats = [(1, 2), (3, 4)]
else:
    rows = int(input("Enter number of Rows in Examination Hall: ").strip())
    cols = int(input("Enter number of Columns in Examination Hall: ").strip())
    dept_a_name = input("Enter Department A code (e.g. CSE): ").strip().upper()
    count_a = int(input("Enter number of students in " + dept_a_name + ": ").strip())
    students_a = []
    for i in range(count_a):
        students_a.append(input(f"  Roll No for {dept_a_name} student #{i+1}: ").strip())
        
    dept_b_name = input("Enter Department B code (e.g. ECE): ").strip().upper()
    count_b = int(input("Enter number of students in " + dept_b_name + ": ").strip())
    students_b = []
    for i in range(count_b):
        students_b.append(input(f"  Roll No for {dept_b_name} student #{i+1}: ").strip())
        
    num_blocked = int(input("Enter number of blocked/reserved seats (0 if none): ").strip())
    blocked_seats = []
    for i in range(num_blocked):
        r_b = int(input(f"  Blocked seat #{i+1} row (0 to {rows-1}): ").strip())
        c_b = int(input(f"  Blocked seat #{i+1} col (0 to {cols-1}): ").strip())
        blocked_seats.append((r_b, c_b))

total_capacity = rows * cols
usable_capacity = total_capacity - len(blocked_seats)
total_students = len(students_a) + len(students_b)

print("\n" + "-" * 70)
print("STAGE 1: CAPACITY & ALTERNATION VALIDATION")
print("-" * 70)
print("Total Hall Seats     : " + str(total_capacity))
print("Blocked/Broken Seats : " + str(len(blocked_seats)))
print("Usable Seats         : " + str(usable_capacity))
print("Total Candidates     : " + str(total_students) + " (" + dept_a_name + ": " + str(len(students_a)) + ", " + dept_b_name + ": " + str(len(students_b)) + ")")

if total_students > usable_capacity:
    print("\n[ERROR] Hall capacity exceeded! Requires " + str(total_students) + " usable seats, but only " + str(usable_capacity) + " available.")
else:
    print("\n[VALIDATION SUCCESS] Hall capacity is sufficient.")

# Stage 2: Seating Matrix Generation using Nested Loops
# Initializing 2D Matrix (List of Lists)
seating_matrix = []
for r in range(rows):
    row_list = []
    for c in range(cols):
        row_list.append("---")
    seating_matrix.append(row_list)

# Mark Blocked/Reserved Seats
for seat_tuple in blocked_seats:
    (br, bc) = seat_tuple
    if 0 <= br < rows and 0 <= bc < cols:
        seating_matrix[br][bc] = "[BLOCKED]"

# Pointer indices for student lists
idx_a = 0
idx_b = 0

# Nested Loop Generation with Alternation Constraint
# Cell (r, c) parity: (r + c) % 2 == 0 gets Dept A, (r + c) % 2 == 1 gets Dept B
for r in range(rows):
    for c in range(cols):
        # Skip blocked seat
        if seating_matrix[r][c] == "[BLOCKED]":
            continue
            
        if (r + c) % 2 == 0:
            if idx_a < len(students_a):
                seating_matrix[r][c] = students_a[idx_a]
                idx_a = idx_a + 1
            else:
                seating_matrix[r][c] = "[EMPTY]"
        else:
            if idx_b < len(students_b):
                seating_matrix[r][c] = students_b[idx_b]
                idx_b = idx_b + 1
            else:
                seating_matrix[r][c] = "[EMPTY]"

print("\n" + "-" * 70)
print("STAGE 2: GENERATED EXAMINATION SEATING GRID")
print("-" * 70)

# Print Column Header
header_str = "        "
for c in range(cols):
    header_str = header_str + f"Col {c:<6} "
print(header_str)
print("        " + "-" * (cols * 10))

for r in range(rows):
    row_str = f"Row {r:<3} | "
    for c in range(cols):
        seat_val = seating_matrix[r][c]
        row_str = row_str + f"{seat_val:<9} "
    print(row_str)

print("-" * 70)

# Stage 3: Automated Adjacency Malpractice Validation
print("\n" + "-" * 70)
print("STAGE 3: ADJACENCY & MALPRACTICE AUDIT")
print("-" * 70)

violations_found = 0

# Check adjacent cells: horizontal (c and c+1) and vertical (r and r+1)
for r in range(rows):
    for c in range(cols):
        current_seat = seating_matrix[r][c]
        if current_seat == "[EMPTY]" or current_seat == "[BLOCKED]":
            continue
            
        # Extract dept prefix (first 2 characters)
        current_dept = current_seat[:2]
        
        # Check Right Neighbor
        if c + 1 < cols:
            right_seat = seating_matrix[r][c + 1]
            if right_seat != "[EMPTY]" and right_seat != "[BLOCKED]":
                right_dept = right_seat[:2]
                if current_dept == right_dept:
                    print(f"  [VIOLATION] Horizontal adjacency: ({r},{c}) '{current_seat}' & ({r},{c+1}) '{right_seat}'")
                    violations_found = violations_found + 1
                    
        # Check Down Neighbor
        if r + 1 < rows:
            down_seat = seating_matrix[r + 1][c]
            if down_seat != "[EMPTY]" and down_seat != "[BLOCKED]":
                down_dept = down_seat[:2]
                if current_dept == down_dept:
                    print(f"  [VIOLATION] Vertical adjacency: ({r},{c}) '{current_seat}' & ({r+1},{c}) '{down_seat}'")
                    violations_found = violations_found + 1

if violations_found == 0:
    print("  [AUDIT PASSED] Zero adjacency violations detected. Anti-cheating alternating constraint verified!")
else:
    print(f"  [AUDIT FAILED] Total violations detected: {violations_found}")

# Seating Allocation Summary
allocated_a = idx_a
allocated_b = idx_b
unseated_a = len(students_a) - idx_a
unseated_b = len(students_b) - idx_b
empty_seats = 0
for r in range(rows):
    for c in range(cols):
        if seating_matrix[r][c] == "[EMPTY]":
            empty_seats = empty_seats + 1

print("\n" + "=" * 70)
print("EXAMINATION SEATING SUMMARY METRICS")
print("=" * 70)
print(f"Total Hall Dimensions : {rows} Rows x {cols} Columns")
print(f"Total Seat Capacity   : {total_capacity}")
print(f"Blocked Seats         : {len(blocked_seats)}")
print(f"{dept_a_name} Seated       : {allocated_a} / {len(students_a)} (Unseated: {unseated_a})")
print(f"{dept_b_name} Seated       : {allocated_b} / {len(students_b)} (Unseated: {unseated_b})")
print(f"Empty Desks Remaining : {empty_seats}")
seat_density = round(((allocated_a + allocated_b) / usable_capacity) * 100, 2)
print(f"Usable Seat Density   : {seat_density}%")
print("=" * 70)
