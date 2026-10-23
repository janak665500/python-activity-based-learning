# Case Study 56: Student Group Formation with Score Balancing
# Allowed Concepts: Variables, Data Types, Operators, Conditionals, Loops, Strings, Lists, Tuples & Unpacking
# Prohibited: Functions, Classes/OOP, Dictionaries, External Libraries (numpy, statistics, itertools)

print("=" * 75)
print("     STUDENT PROJECT GROUP FORMATION & SCORE BALANCING (Case Study 56)")
print("=" * 75)

mode_input = input("Enter '1' for interactive student entry or '0' for Automated Test Dataset: ").strip()

# Student tuple structure: (roll_no, name, score)
students = []

if mode_input == "" or mode_input == "0" or mode_input.lower() == "demo":
    print("\n[Loading Benchmark Class Dataset: 12 Students to be split into 3 Balanced Teams]")
    num_teams = 3
    students.append(("26CS01", "Aditya Sharma", 96.0))
    students.append(("26CS02", "Bhavya Sri", 92.5))
    students.append(("26CS03", "Charan Teja", 89.0))
    students.append(("26CS04", "Divya Vani", 85.0))
    students.append(("26CS05", "Eswar Kumar", 82.0))
    students.append(("26CS06", "Farhana Anjum", 78.5))
    students.append(("26CS07", "Ganesh Vardhan", 75.0))
    students.append(("26CS08", "Harika Devi", 71.5))
    students.append(("26CS09", "Imran Pasha", 68.0))
    students.append(("26CS10", "Jaswanth Sai", 64.0))
    students.append(("26CS11", "Kavya Sree", 60.5))
    students.append(("26CS12", "Lokesh Naidu", 54.0))
else:
    num_teams = int(input("Enter number of project teams to create (K): ").strip())
    n_students = int(input("Enter total number of students: ").strip())
    for i in range(n_students):
        r_no = input(f"  Roll Number for Student #{i+1}: ").strip()
        s_name = input(f"  Student Name for Student #{i+1}: ").strip()
        sc = float(input(f"  Academic Assessment Score (0-100): ").strip())
        students.append((r_no, s_name, sc))

total_students = len(students)

print("\n" + "-" * 75)
print("STAGE 1: SCORE SORTING VIA NESTED LOOP BUBBLE SORT")
print("-" * 75)

# Sort students in descending order of their academic score
for i in range(total_students - 1):
    for j in range(0, total_students - i - 1):
        if students[j][2] < students[j + 1][2]:
            temp = students[j]
            students[j] = students[j + 1]
            students[j + 1] = temp

print("Sorted Student Pool (High to Low Scores):")
for rk in range(total_students):
    (r_no, s_name, sc) = students[rk]
    print(f"  Rank {rk+1:>2}: {r_no} | {s_name:<16} | Score: {sc:.1f}")

# ---------------------------------------------------------
# STAGE 2: GREEDY CAPACITY-CONSTRAINED SCORE BALANCING
# ---------------------------------------------------------
# Team representation using nested lists:
# team_members: List of lists containing student tuples
# team_scores: List of float aggregates
# team_capacities: Maximum members per team
max_per_team = (total_students + num_teams - 1) // num_teams

team_members = []
team_scores = []
for t in range(num_teams):
    team_members.append([])
    team_scores.append(0.0)

# Greedy Distribution:
# For each student in sorted order, allocate them to the team that:
# 1. Currently has fewer than max_per_team members.
# 2. Has the minimum current cumulative score among all valid teams.
for s_idx in range(total_students):
    student_tuple = students[s_idx]
    (r_no, s_name, sc) = student_tuple
    
    best_team_idx = -1
    min_score = 9999999.0
    
    for t_idx in range(num_teams):
        if len(team_members[t_idx]) < max_per_team:
            if team_scores[t_idx] < min_score:
                min_score = team_scores[t_idx]
                best_team_idx = t_idx
                
    # Place student into best team
    team_members[best_team_idx].append(student_tuple)
    team_scores[best_team_idx] = team_scores[best_team_idx] + sc

# ---------------------------------------------------------
# STAGE 3: TEAM REPORTING & BALANCE ANALYTICS
# ---------------------------------------------------------
print("\n" + "=" * 75)
print("STAGE 2: FINAL ALLOCATED PROJECT TEAMS & COMPOSITION")
print("=" * 75)

total_all_scores = 0.0
for t_idx in range(num_teams):
    members = team_members[t_idx]
    tot_sc = round(team_scores[t_idx], 2)
    avg_sc = round(tot_sc / len(members), 2)
    total_all_scores = total_all_scores + tot_sc
    
    print(f"\n[TEAM {t_idx + 1}] | Total Score: {tot_sc:.2f} | Average Score: {avg_sc:.2f} | Size: {len(members)}")
    print(f"  {'Roll No':<10} {'Student Name':<18} {'Individual Score':<16}")
    print("  " + "-" * 45)
    for m in members:
        (r_no, s_name, sc) = m
        print(f"  {r_no:<10} {s_name:<18} {sc:<16.1f}")

# Group Disparity / Variance Analysis
min_team_score = team_scores[0]
max_team_score = team_scores[0]
for sc in team_scores:
    if sc < min_team_score:
        min_team_score = sc
    if sc > max_team_score:
        max_team_score = sc

score_delta = round(max_team_score - min_team_score, 2)
ideal_target_score = round(total_all_scores / num_teams, 2)

print("\n" + "=" * 75)
print("STAGE 3: BALANCE AUDIT & STATISTICAL METRICS")
print("=" * 75)
print(f"Total Student Cohort Size  : {total_students}")
print(f"Configured Teams (K)       : {num_teams}")
print(f"Ideal Aggregate per Team   : {ideal_target_score}")
print(f"Highest Team Aggregate     : {max_team_score:.2f}")
print(f"Lowest Team Aggregate      : {min_team_score:.2f}")
print(f"Score Spread / Disparity   : {score_delta} points")

# Calculate Mean Absolute Deviation (MAD) across team totals
deviation_sum = 0.0
for sc in team_scores:
    diff = sc - ideal_target_score
    if diff < 0:
        diff = -diff
    deviation_sum = deviation_sum + diff
avg_deviation = round(deviation_sum / num_teams, 2)

print(f"Average Team Deviation     : {avg_deviation} points from target")
if score_delta <= 5.0:
    print("Balance Quality Assessment : [EXCELLENT] Uniformly balanced groups.")
elif score_delta <= 12.0:
    print("Balance Quality Assessment : [GOOD] Acceptable equitable distribution.")
else:
    print("Balance Quality Assessment : [FAIR] High initial student score variance.")
print("=" * 75)
