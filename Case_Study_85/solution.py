# Case Study 85: Smart Classroom Timetable Allocation
# Allowed Concepts: Variables, Data Types, Operators, Conditionals, Loops, Strings, Lists, Tuples & Unpacking
# Prohibited: Functions, Classes/OOP, Dictionaries, External Libraries

print("=" * 80)
print("       SMART CLASSROOM TIMETABLE ALLOCATION ENGINE (Case Study 85)")
print("=" * 80)

mode_input = input("Enter '1' for interactive entry or '0' for Automated Test Dataset: ").strip()

# Available Rooms: (room_id, capacity, has_projector)
rooms = []

# Courses Catalog: (course_code, course_title, enrolled_students, requires_projector, instructor)
courses = []

# Timetable Booking Requests: (course_code, room_id, day, start_hour, duration)
# Hours in 24-hr format (e.g. 9 for 9:00 AM, duration in hours)
bookings = []

if mode_input == "" or mode_input == "0" or mode_input.lower() == "demo":
    print("\n[Loading Standard Engineering Department Schedule Dataset...]")
    # 3 Rooms
    rooms.append(("LH101", 60, True))
    rooms.append(("LH102", 40, False))
    rooms.append(("LAB201", 30, True))

    # 5 Courses
    courses.append(("CS101", "Problem Solving with Python", 55, True, "Dr. Ramesh"))
    courses.append(("EC102", "Digital Logic Design", 35, False, "Prof. Anitha"))
    courses.append(("CS103", "Data Structures Lab", 28, True, "Dr. Ramesh")) # Same instructor as CS101
    courses.append(("MA104", "Engineering Mathematics-I", 58, False, "Dr. Sudha"))
    courses.append(("HS105", "Professional Communication", 45, True, "Prof. John")) # Projector needed, 45 students

    # 6 Proposed Bookings (Contains deliberate test clashes to verify audit logic):
    # 1. Valid booking
    bookings.append(("CS101", "LH101", "Monday", 9, 2))      # Mon 9:00 - 11:00
    # 2. Room Clash with booking #1 in LH101 on Mon 10:00 - 12:00
    bookings.append(("MA104", "LH101", "Monday", 10, 2))     # Mon 10:00 - 12:00 (ROOM CLASH with CS101)
    # 3. Valid booking in LH102
    bookings.append(("EC102", "LH102", "Monday", 9, 2))      # Mon 9:00 - 11:00
    # 4. Instructor Clash: Dr. Ramesh teaching CS103 while already booked for CS101 Mon 9:00-11:00
    bookings.append(("CS103", "LAB201", "Monday", 9, 2))     # Mon 9:00 - 11:00 (INSTRUCTOR CLASH: Dr. Ramesh)
    # 5. Facility Mismatch: HS105 requires projector, but LH102 has NO projector
    # Also Capacity Overrun: HS105 has 45 students, but LH102 capacity is 40
    bookings.append(("HS105", "LH102", "Tuesday", 14, 2))    # Tue 14:00 - 16:00 (CAPACITY & PROJECTOR VIOLATION)
    # 6. Valid booking on Tuesday
    bookings.append(("CS101", "LH101", "Tuesday", 10, 2))     # Tue 10:00 - 12:00
else:
    # Interactive input
    num_rooms = int(input("Enter number of lecture rooms / labs: ").strip())
    for i in range(num_rooms):
        r_id = input(f"  Room ID #{i+1} (e.g. LH101): ").strip().upper()
        r_cap = int(input(f"  Capacity of {r_id}: ").strip())
        r_proj = input(f"  Does {r_id} have projector? (yes/no): ").strip().lower().startswith("y")
        rooms.append((r_id, r_cap, r_proj))

    num_courses = int(input("\nEnter number of courses: ").strip())
    for i in range(num_courses):
        c_code = input(f"  Course Code #{i+1} (e.g. CS101): ").strip().upper()
        c_title = input(f"  Course Title: ").strip()
        c_enrolled = int(input(f"  Number of students enrolled: ").strip())
        c_proj = input(f"  Requires projector? (yes/no): ").strip().lower().startswith("y")
        c_inst = input(f"  Faculty Instructor Name: ").strip()
        courses.append((c_code, c_title, c_enrolled, c_proj, c_inst))

    num_b = int(input("\nEnter number of booking requests: ").strip())
    for i in range(num_b):
        b_code = input(f"  Booking #{i+1} Course Code: ").strip().upper()
        b_room = input(f"  Room ID: ").strip().upper()
        b_day = input(f"  Day of Week (e.g. Monday): ").strip().capitalize()
        b_start = int(input(f"  Start Hour (e.g. 9 for 9 AM): ").strip())
        b_dur = int(input(f"  Duration (hours): ").strip())
        bookings.append((b_code, b_room, b_day, b_start, b_dur))

print("\n" + "-" * 80)
print("STAGE 1: VERIFYING FACILITY & CAPACITY COMPLIANCE")
print("-" * 80)

approved_schedule = []
rejected_bookings = []

# Process each booking request
for b_idx in range(len(bookings)):
    b_req = bookings[b_idx]
    (b_code, b_room, b_day, b_start, b_dur) = b_req
    b_end = b_start + b_dur
    
    # 1. Lookup Course Information (Linear Search without Dictionaries)
    course_found = False
    c_title = ""
    c_enrolled = 0
    c_proj = False
    c_inst = ""
    for c in courses:
        if c[0] == b_code:
            course_found = True
            c_title = c[1]
            c_enrolled = c[2]
            c_proj = c[3]
            c_inst = c[4]
            break
            
    # 2. Lookup Room Information
    room_found = False
    r_cap = 0
    r_proj = False
    for r in rooms:
        if r[0] == b_room:
            room_found = True
            r_cap = r[1]
            r_proj = r[2]
            break
            
    is_valid = True
    issues = []
    
    if not course_found:
        is_valid = False
        issues.append(f"Course code '{b_code}' not found in academic catalog")
        
    if not room_found:
        is_valid = False
        issues.append(f"Room '{b_room}' not found in campus inventory")
        
    if course_found and room_found:
        # Check Capacity
        if c_enrolled > r_cap:
            is_valid = False
            issues.append(f"Capacity exceeded: {c_enrolled} students enrolled, but {b_room} capacity is {r_cap}")
            
        # Check Projector Requirement
        if c_proj and not r_proj:
            is_valid = False
            issues.append(f"Facility mismatch: {b_code} requires projector, but {b_room} has no projector")
            
        # 3. Check Clashes Against Already Approved Schedule
        # An interval [s1, e1) overlaps with [s2, e2) if max(s1, s2) < min(e1, e2)
        for app in approved_schedule:
            # Structure of app: (code, title, room, day, start, end, enrolled, instructor)
            (a_code, a_title, a_room, a_day, a_start, a_end, a_enrolled, a_inst) = app
            
            if a_day == b_day:
                # Calculate time overlap
                latest_start = b_start if b_start > a_start else a_start
                earliest_end = b_end if b_end < a_end else a_end
                
                if latest_start < earliest_end:
                    # Time overlap detected!
                    # Check Room Conflict
                    if a_room == b_room:
                        is_valid = False
                        issues.append(f"Room collision: {b_room} already booked by {a_code} ({a_start}:00-{a_end}:00)")
                        
                    # Check Faculty Instructor Conflict
                    if a_inst == c_inst:
                        is_valid = False
                        issues.append(f"Faculty clash: {c_inst} already teaching {a_code} at ({a_start}:00-{a_end}:00)")
                        
    if is_valid:
        approved_schedule.append((b_code, c_title, b_room, b_day, b_start, b_end, c_enrolled, c_inst))
        print(f"  [APPROVED] {b_code:<6} in {b_room:<6} on {b_day:<8} ({b_start:02d}:00 - {b_end:02d}:00) | {c_inst}")
    else:
        rejected_bookings.append((b_code, b_room, b_day, b_start, b_end, issues))
        print(f"  [REJECTED] {b_code:<6} in {b_room:<6} on {b_day:<8} ({b_start:02d}:00 - {b_end:02d}:00)")
        for iss in issues:
            print(f"             [-] {iss}")

# ---------------------------------------------------------
# STAGE 2: TIMETABLE SCHEDULE & ROOM UTILIZATION ANALYTICS
# ---------------------------------------------------------
print("\n" + "=" * 80)
print("STAGE 2: MASTER CONFLICT-FREE TIMETABLE SCHEDULE")
print("=" * 80)
print(f"{'Day':<10} {'Time Slot':<15} {'Room':<8} {'Code':<7} {'Course Title':<28} {'Instructor':<15}")
print("-" * 80)
for sch in approved_schedule:
    (code, title, room, day, s_hr, e_hr, enr, inst) = sch
    slot_str = f"{s_hr:02d}:00 - {e_hr:02d}:00"
    print(f"{day:<10} {slot_str:<15} {room:<8} {code:<7} {title:<28} {inst:<15}")

print("\n" + "=" * 80)
print("STAGE 3: CLASSROOM UTILIZATION & CAPACITY EFFICIENCY")
print("=" * 80)
print(f"{'Room ID':<10} {'Capacity':<10} {'Projector':<12} {'Booked Hours':<14} {'Seat Utilization'}")
print("-" * 80)

total_booked_hours_all = 0
for r in rooms:
    (r_id, r_cap, r_proj) = r
    proj_str = "YES" if r_proj else "NO"
    
    room_hours = 0
    total_seat_hours_used = 0
    
    for sch in approved_schedule:
        if sch[2] == r_id:
            dur = sch[5] - sch[4]
            room_hours = room_hours + dur
            total_seat_hours_used = total_seat_hours_used + (sch[6] * dur)
            
    total_booked_hours_all = total_booked_hours_all + room_hours
    
    if room_hours > 0:
        possible_seat_hours = r_cap * room_hours
        util_pct = round((total_seat_hours_used / possible_seat_hours) * 100, 2)
        util_str = f"{util_pct}%"
    else:
        util_str = "0.0% (Idle)"
        
    print(f"{r_id:<10} {r_cap:<10} {proj_str:<12} {room_hours:<14} {util_str}")

print("\n" + "=" * 80)
print("ALLOCATION SUMMARY METRICS")
print("=" * 80)
print(f"Total Booking Requests Processed : {len(bookings)}")
print(f"Approved Conflict-Free Classes  : {len(approved_schedule)}")
print(f"Rejected / Conflicting Bookings : {len(rejected_bookings)}")
print(f"Total Weekly Instructional Hours: {total_booked_hours_all} hours")
print("=" * 80)
