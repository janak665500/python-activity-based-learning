# Case Study 100: Comprehensive Smart Campus Management Simulation (Capstone)
# Allowed Concepts: Variables, Data Types, Operators, Conditionals, Loops (while, for, nested), Strings, Lists, Tuples & Unpacking
# Prohibited: Functions, Classes/OOP, Dictionaries, External Libraries

print("=" * 80)
print("     COMPREHENSIVE SMART CAMPUS MANAGEMENT SIMULATION (Case Study 100)")
print("=" * 80)

# =========================================================
# INITIALIZING CENTRAL CAMPUS REPOSITORIES (STATE VARIABLES)
# =========================================================

# 1. Student Database: List of tuples
# (roll_no, full_name, branch, sem, fee_paid, fee_due, attendance_pct)
students = [
    ("26CS01", "Aarav Sharma", "CSE", 2, 65000.0, 0.0, 88.5),
    ("26EC02", "Bhavna Patel", "ECE", 2, 65000.0, 0.0, 91.0),
    ("26CS03", "Chirag Verma", "CSE", 2, 45000.0, 20000.0, 71.0),  # Low attendance (<75%) & fee due
    ("26IT04", "Deepa Rao", "IT", 2, 65000.0, 0.0, 68.0),          # Low attendance (<75%)
    ("26ME05", "Esha Reddy", "MECH", 2, 50000.0, 15000.0, 82.0)
]

# 2. Hostel Allocation 2D Matrix (3 Floors x 4 Rooms per Floor)
# Floors: 0 (Ground), 1 (First), 2 (Second)
hostel_grid = [
    ["26CS01", "[VACANT]", "26EC02", "[VACANT]"],
    ["26CS03", "[VACANT]", "[VACANT]", "26IT04"],
    ["[VACANT]", "26ME05", "[VACANT]", "[VACANT]"]
]
HOSTEL_FLOORS = 3
HOSTEL_ROOMS_PER_FLOOR = 4

# 3. Library Issue Catalog: List of tuples
# (roll_no, book_title, days_held)
library_loans = [
    ("26CS01", "Python Programming ABL", 10),
    ("26CS03", "Data Structures in C", 21),  # Overdue by 7 days
    ("26EC02", "Digital Electronics", 14),   # On time
    ("26IT04", "Computer Networks", 25)      # Overdue by 11 days
]
LOAN_LIMIT_DAYS = 14
FINE_PER_DAY = 5.0 # Rs. 5 per overdue day

# 4. RFID Gate Security Access Logs: List of tuples
# (time_str, roll_no, gate_name, direction, is_curfew_violation)
# Curfew is 21:00 (9:00 PM). Entries after 21:00 are violations.
gate_logs = [
    ("17:45", "26CS01", "Main Gate", "EXIT", False),
    ("19:30", "26CS01", "Main Gate", "ENTRY", False),
    ("21:40", "26CS03", "Hostel Gate", "ENTRY", True),   # Curfew violation
    ("22:15", "26IT04", "Main Gate", "ENTRY", True)      # Curfew violation
]

# Check if automated benchmark demo mode is requested
mode_input = input("Enter '1' for Interactive Menu Mode or '0' for Automated Capstone Execution: ").strip()
auto_demo = (mode_input == "" or mode_input == "0" or mode_input.lower() == "demo")

# Interactive / Simulation Loop Control
is_running = True
simulation_step = 1

while is_running:
    if auto_demo:
        choice = str(simulation_step)
        print(f"\n[AUTO-SIMULATION TRIGGER: Executing Subsystem Menu Option {choice}]")
    else:
        print("\n" + "=" * 80)
        print("                 SMART CAMPUS EXECUTIVE DASHBOARD MENU")
        print("=" * 80)
        print("  1. Student Academic & Fee Reconciliation Subsystem")
        print("  2. Smart Hostel 2D Matrix Allocation & Occupancy Subsystem")
        print("  3. Campus Library Loan Circulation & Fine Audit Subsystem")
        print("  4. Security RFID Gate Access & Curfew Breach Subsystem")
        print("  5. Consolidated Executive Campus Health KPI Report")
        print("  0. Terminate Campus Simulation Session")
        print("=" * 80)
        choice = input("Enter your subsystem choice (0-5): ").strip()

    # -----------------------------------------------------
    # OPTION 1: STUDENT ACADEMICS, FEES & ATTENDANCE AUDIT
    # -----------------------------------------------------
    if choice == "1":
        print("\n" + "-" * 80)
        print("SUBSYSTEM 1: STUDENT ROSTER, ACADEMICS & DETENTION AUDIT")
        print("-" * 80)
        print(f"{'Roll No':<8} {'Student Name':<16} {'Branch':<8} {'Sem':<5} {'Fee Paid':<11} {'Fee Due':<10} {'Attendance':<12} {'Status'}")
        print("-" * 80)
        
        detention_count = 0
        total_due_all = 0.0
        total_paid_all = 0.0
        
        for st in students:
            (r_no, s_nm, br, sem, paid, due, att) = st
            total_paid_all = total_paid_all + paid
            total_due_all = total_due_all + due
            
            if att < 75.0:
                detention_status = "[DETAINED]"
                detention_count = detention_count + 1
            else:
                detention_status = "[ELIGIBLE]"
                
            print(f"{r_no:<8} {s_nm:<16} {br:<8} {sem:<5} Rs.{paid:<8.0f} Rs.{due:<7.0f} {att:<11.1f}% {detention_status}")
            
        print("-" * 80)
        print(f"Total Cohort: {len(students)} | Detained (Attendance < 75%): {detention_count} | Total Fees Due: Rs. {total_due_all:.2f}")

    # -----------------------------------------------------
    # OPTION 2: HOSTEL ROOM 2D MATRIX ALLOCATION
    # -----------------------------------------------------
    elif choice == "2":
        print("\n" + "-" * 80)
        print("SUBSYSTEM 2: SMART HOSTEL 2D MATRIX ROOM OCCUPANCY GRID")
        print("-" * 80)
        
        hdr = "        "
        for r_col in range(HOSTEL_ROOMS_PER_FLOOR):
            hdr = hdr + f"Room {r_col + 1:<8} "
        print(hdr)
        print("        " + "-" * (HOSTEL_ROOMS_PER_FLOOR * 14))
        
        occupied_rooms = 0
        vacant_rooms = 0
        
        for fl_idx in range(HOSTEL_FLOORS):
            floor_name = f"Floor {fl_idx} | "
            row_str = floor_name
            for rm_idx in range(HOSTEL_ROOMS_PER_FLOOR):
                occupant = hostel_grid[fl_idx][rm_idx]
                if occupant == "[VACANT]":
                    vacant_rooms = vacant_rooms + 1
                    cell_text = "[VACANT]"
                else:
                    occupied_rooms = occupied_rooms + 1
                    cell_text = occupant
                row_str = row_str + f"{cell_text:<13} "
            print(row_str)
            
        total_hostel_capacity = HOSTEL_FLOORS * HOSTEL_ROOMS_PER_FLOOR
        occupancy_rate = round((occupied_rooms / total_hostel_capacity) * 100, 2)
        print("-" * 80)
        print(f"Total Rooms: {total_hostel_capacity} | Occupied: {occupied_rooms} | Vacant: {vacant_rooms} | Occupancy Rate: {occupancy_rate}%")

    # -----------------------------------------------------
    # OPTION 3: LIBRARY CIRCULATION & PENALTY AUDIT
    # -----------------------------------------------------
    elif choice == "3":
        print("\n" + "-" * 80)
        print("SUBSYSTEM 3: CAMPUS LIBRARY LOANS, OVERDUE & FINE AUDIT")
        print("-" * 80)
        print(f"{'Borrower':<10} {'Book Title':<28} {'Days Out':<10} {'Allowed':<10} {'Overdue':<10} {'Fine (Rs.)'}")
        print("-" * 80)
        
        total_fines_accrued = 0.0
        overdue_books_count = 0
        
        for loan in library_loans:
            (r_no, b_title, days) = loan
            if days > LOAN_LIMIT_DAYS:
                overdue_days = days - LOAN_LIMIT_DAYS
                fine = overdue_days * FINE_PER_DAY
                overdue_books_count = overdue_books_count + 1
            else:
                overdue_days = 0
                fine = 0.0
                
            total_fines_accrued = total_fines_accrued + fine
            fine_str = f"Rs. {fine:.2f}" if fine > 0 else "NIL"
            print(f"{r_no:<10} {b_title:<28} {days:<10} {LOAN_LIMIT_DAYS:<10} {overdue_days:<10} {fine_str}")
            
        print("-" * 80)
        print(f"Total Active Loans: {len(library_loans)} | Overdue Returns: {overdue_books_count} | Total Outstanding Fines: Rs. {total_fines_accrued:.2f}")

    # -----------------------------------------------------
    # OPTION 4: GATE RFID ACCESS LOGS & CURFEW AUDIT
    # -----------------------------------------------------
    elif choice == "4":
        print("\n" + "-" * 80)
        print("SUBSYSTEM 4: RFID SECURITY GATE TRANSIT & CURFEW BREACH AUDIT")
        print("-" * 80)
        print(f"{'Time':<8} {'Roll No':<10} {'Gate Location':<16} {'Transit':<10} {'Security Compliance'}")
        print("-" * 80)
        
        curfew_breaches = 0
        for log in gate_logs:
            (tm, r_no, gate, direction, is_breach) = log
            if is_breach:
                curfew_breaches = curfew_breaches + 1
                status = "[ALERT: LATE NIGHT CURFEW BREACH]"
            else:
                status = "[AUTHORIZED TRANSIT]"
            print(f"{tm:<8} {r_no:<10} {gate:<16} {direction:<10} {status}")
            
        print("-" * 80)
        print(f"Total RFID Events: {len(gate_logs)} | Curfew Security Breaches: {curfew_breaches}")

    # -----------------------------------------------------
    # OPTION 5: CONSOLIDATED EXECUTIVE CAMPUS HEALTH DASHBOARD
    # -----------------------------------------------------
    elif choice == "5":
        print("\n" + "=" * 80)
        print("           CAMPUS-WIDE CONSOLIDATED EXECUTIVE KPI SCORECARD")
        print("=" * 80)
        
        # Calculate summary cross-subsystem metrics
        tot_students = len(students)
        detained = 0
        fees_collected = 0.0
        fees_outstanding = 0.0
        for st in students:
            fees_collected = fees_collected + st[4]
            fees_outstanding = fees_outstanding + st[5]
            if st[6] < 75.0:
                detained = detained + 1
                
        occ_beds = 0
        tot_beds = HOSTEL_FLOORS * HOSTEL_ROOMS_PER_FLOOR
        for r_row in hostel_grid:
            for cell in r_row:
                if cell != "[VACANT]":
                    occ_beds = occ_beds + 1
                    
        overdue_books = 0
        library_rev = 0.0
        for l in library_loans:
            if l[2] > LOAN_LIMIT_DAYS:
                overdue_books = overdue_books + 1
                library_rev = library_rev + ((l[2] - LOAN_LIMIT_DAYS) * FINE_PER_DAY)
                
        breach_count = 0
        for g in gate_logs:
            if g[4]:
                breach_count = breach_count + 1
                
        print(f"Total Student Body Enrolled         : {tot_students} Students")
        print(f"Examination Eligible Rate           : {round(((tot_students - detained) / tot_students) * 100, 2)}% ({tot_students - detained} eligible, {detained} detained)")
        print(f"Total Institutional Fees Collected : Rs. {fees_collected:,.2f}")
        print(f"Pending Outstanding Tuition Dues    : Rs. {fees_outstanding:,.2f}")
        print(f"Campus Hostel Occupancy Percentage  : {round((occ_beds / tot_beds) * 100, 2)}% ({occ_beds}/{tot_beds} rooms booked)")
        print(f"Active Library Circulation Overdue  : {overdue_books} titles (Pending Fines: Rs. {library_rev:.2f})")
        print(f"Gate Curfew Security Violations     : {breach_count} infractions logged")
        print("=" * 80)
        print("Overall Campus Operational Status   : [NOMINAL - REGULAR OPERATIONS ACTIVE]")
        print("=" * 80)

    # -----------------------------------------------------
    # OPTION 0: TERMINATE / EXIT
    # -----------------------------------------------------
    elif choice == "0":
        print("\n[Terminating Smart Campus Simulation Engine. Session Closed.]")
        is_running = False
        
    else:
        print("\n[INVALID SELECTION] Please enter a valid menu option (0 to 5).")

    # In automated mode, cycle through all subsystems 1 through 5 and then exit
    if auto_demo:
        simulation_step = simulation_step + 1
        if simulation_step > 5:
            is_running = False

print("\n" + "=" * 80)
print("CAPSTONE SIMULATION RUN COMPLETED SUCCESSFULLY")
print("=" * 80)
