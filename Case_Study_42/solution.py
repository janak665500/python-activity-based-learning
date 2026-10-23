# Case Study 42: Student Marks Matrix Analysis
# Allowed Concepts: Variables, Data Types, Operators, Conditionals, Loops, Strings, Lists, Tuples & Unpacking
# Prohibited: Functions, Classes/OOP, Dictionaries, External Libraries (numpy, pandas, statistics)

print("=" * 75)
print("        ACADEMIC MARKS MATRIX ANALYTICS ENGINE (Case Study 42)")
print("=" * 75)

mode_input = input("Enter '1' for interactive entry or '0' for Automated Test Dataset: ").strip()

subjects = ["Mathematics", "Physics", "Chemistry", "Python Prog", "Data Struct"]
num_subjects = len(subjects)

# Matrix rows structure: [student_id, student_name, m1, m2, m3, m4, m5]
student_matrix = []

if mode_input == "" or mode_input == "0" or mode_input.lower() == "demo":
    print("\n[Loading Benchmark Academic Class Matrix (6 Students x 5 Subjects)...]")
    student_matrix.append(["STU101", "Aakash Gupta", 88.0, 92.0, 79.0, 95.0, 84.0])
    student_matrix.append(["STU102", "Bhavna Joshi", 94.0, 89.0, 91.0, 96.0, 90.0])
    student_matrix.append(["STU103", "Chetan Reddy", 58.0, 62.0, 54.0, 70.0, 65.0])
    student_matrix.append(["STU104", "Deepa Sharma", 74.0, 36.0, 68.0, 82.0, 71.0]) # Fails in Physics (36 < 40)
    student_matrix.append(["STU105", "Ehsaan Khan", 91.0, 85.0, 88.0, 92.0, 87.0])
    student_matrix.append(["STU106", "Fatima Zehra", 42.0, 48.0, 50.0, 55.0, 45.0])
else:
    n_students = int(input("Enter total number of students: ").strip())
    for i in range(n_students):
        print(f"\nEntering record for Student #{i+1}:")
        s_id = input("  Roll / Student ID: ").strip()
        s_name = input("  Full Name: ").strip()
        row = [s_id, s_name]
        for sub in subjects:
            val = float(input(f"  Marks in {sub} (0-100): ").strip())
            row.append(val)
        student_matrix.append(row)

total_students = len(student_matrix)

# ---------------------------------------------------------
# STAGE 1: ROW-WISE STUDENT PERFORMANCE COMPUTATION
# ---------------------------------------------------------
# Results list will store:
# (s_id, s_name, total_marks, avg_pct, best_sub, worst_sub, grade, status)
student_results = []

grade_letters = ["O", "A+", "A", "B+", "B", "C", "F"]
grade_counts = [0, 0, 0, 0, 0, 0, 0] # Parallel list tracking grade distribution

class_total_score = 0.0
total_passed_students = 0

for i in range(total_students):
    row = student_matrix[i]
    s_id = row[0]
    s_name = row[1]
    
    # Calculate row aggregates
    row_sum = 0.0
    min_mark = row[2]
    max_mark = row[2]
    min_sub_idx = 0
    max_sub_idx = 0
    has_failed_subject = False
    
    for s_idx in range(num_subjects):
        mark = row[2 + s_idx]
        row_sum = row_sum + mark
        
        if mark < 40.0:
            has_failed_subject = True
            
        if mark > max_mark:
            max_mark = mark
            max_sub_idx = s_idx
            
        if mark < min_mark:
            min_mark = mark
            min_sub_idx = s_idx
            
    avg_pct = round(row_sum / num_subjects, 2)
    class_total_score = class_total_score + avg_pct
    
    # Determine Grade and Status
    if has_failed_subject:
        grade = "F"
        status = "FAIL"
    else:
        status = "PASS"
        total_passed_students = total_passed_students + 1
        if avg_pct >= 90.0:
            grade = "O"
        elif avg_pct >= 80.0:
            grade = "A+"
        elif avg_pct >= 70.0:
            grade = "A"
        elif avg_pct >= 60.0:
            grade = "B+"
        elif avg_pct >= 50.0:
            grade = "B"
        else:
            grade = "C"
            
    # Update grade counts using parallel indexing
    for g_idx in range(len(grade_letters)):
        if grade == grade_letters[g_idx]:
            grade_counts[g_idx] = grade_counts[g_idx] + 1
            
    best_sub = subjects[max_sub_idx] + " (" + str(max_mark) + ")"
    worst_sub = subjects[min_sub_idx] + " (" + str(min_mark) + ")"
    
    student_results.append((s_id, s_name, row_sum, avg_pct, best_sub, worst_sub, grade, status))

# ---------------------------------------------------------
# STAGE 2: COLUMN-WISE SUBJECT ANALYSIS
# ---------------------------------------------------------
# For each subject column: average, highest, lowest, pass rate
subject_analytics = []

hardest_sub_name = ""
hardest_sub_avg = 999.0

easiest_sub_name = ""
easiest_sub_avg = -1.0

for s_idx in range(num_subjects):
    col_sum = 0.0
    col_max = student_matrix[0][2 + s_idx]
    col_min = student_matrix[0][2 + s_idx]
    col_passes = 0
    
    for r_idx in range(total_students):
        val = student_matrix[r_idx][2 + s_idx]
        col_sum = col_sum + val
        if val > col_max:
            col_max = val
        if val < col_min:
            col_min = val
        if val >= 40.0:
            col_passes = col_passes + 1
            
    col_avg = round(col_sum / total_students, 2)
    col_pass_pct = round((col_passes / total_students) * 100, 2)
    
    if col_avg < hardest_sub_avg:
        hardest_sub_avg = col_avg
        hardest_sub_name = subjects[s_idx]
        
    if col_avg > easiest_sub_avg:
        easiest_sub_avg = col_avg
        easiest_sub_name = subjects[s_idx]
        
    subject_analytics.append((subjects[s_idx], col_avg, col_max, col_min, col_pass_pct))

# ---------------------------------------------------------
# STAGE 3: CLASS TOPPER & RANK DETECTION (Nested Loop Sort)
# ---------------------------------------------------------
# Bubble sort student_results by average percentage descending
n = len(student_results)
for i in range(n - 1):
    for j in range(0, n - i - 1):
        if student_results[j][3] < student_results[j + 1][3]:
            temp = student_results[j]
            student_results[j] = student_results[j + 1]
            student_results[j + 1] = temp

# ---------------------------------------------------------
# DISPLAY SECTION: COMPREHENSIVE PERFORMANCE REPORTS
# ---------------------------------------------------------
print("\n" + "=" * 85)
print("STAGE 1: STUDENT-WISE TRANSCRIPT & MERIT RANKING (ROW-WISE TRAVERSAL)")
print("=" * 85)
print(f"{'Rank':<5} {'ID':<8} {'Student Name':<16} {'Total':<7} {'Avg %':<7} {'Grade':<6} {'Status':<6} {'Strongest Subject':<20}")
print("-" * 85)
for rk in range(len(student_results)):
    (s_id, s_name, tot, avg, best, worst, grd, stat) = student_results[rk]
    print(f"{rk+1:<5} {s_id:<8} {s_name:<16} {tot:<7.1f} {avg:<7.2f} {grd:<6} {stat:<6} {best:<20}")

print("\n" + "=" * 85)
print("STAGE 2: SUBJECT-WISE PERFORMANCE & DIFFICULTY METRICS (COLUMN-WISE TRAVERSAL)")
print("=" * 85)
print(f"{'Subject Name':<18} {'Class Avg':<11} {'Highest':<9} {'Lowest':<9} {'Pass Rate':<10} {'Difficulty'}")
print("-" * 85)
for s_info in subject_analytics:
    (sub_name, sub_avg, sub_hi, sub_lo, sub_pr) = s_info
    diff_tag = "Normal"
    if sub_name == hardest_sub_name:
        diff_tag = "[HARDEST]"
    elif sub_name == easiest_sub_name:
        diff_tag = "[EASIEST]"
    print(f"{sub_name:<18} {sub_avg:<11.2f} {sub_hi:<9.1f} {sub_lo:<9.1f} {sub_pr:<9.1f}% {diff_tag}")

print("\n" + "=" * 85)
print("STAGE 3: CLASS-LEVEL OVERALL SUMMARY & GRADE DISTRIBUTION")
print("=" * 85)
class_avg_pct = round(class_total_score / total_students, 2)
class_pass_rate = round((total_passed_students / total_students) * 100, 2)
topper = student_results[0]

print(f"Class Overall Average Score : {class_avg_pct}%")
print(f"Class Overall Pass Rate     : {class_pass_rate}% ({total_passed_students}/{total_students} students)")
print(f"Academic Batch Topper       : {topper[1]} ({topper[0]}) with {topper[3]}% (Total: {topper[2]}/500)")
print(f"Most Demanding Subject      : {hardest_sub_name} (Lowest Class Average: {hardest_sub_avg})")
print(f"Highest Scoring Subject     : {easiest_sub_name} (Highest Class Average: {easiest_sub_avg})")

print("\nGrade Frequency Distribution:")
dist_str = "  "
for g_i in range(len(grade_letters)):
    dist_str = dist_str + f"Grade {grade_letters[g_i]}: {grade_counts[g_i]}  |  "
print(dist_str)
print("=" * 85)
