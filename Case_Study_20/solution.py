# Case Study 20: University Admission Decision Engine
# Allowed Concepts: Variables, Data Types, Operators, Conditionals, Loops, Strings, Lists, Tuples & Unpacking
# Prohibited: Functions, Classes/OOP, Dictionaries, External Libraries (pandas, etc.)

print("=" * 70)
print("       UNIVERSITY ADMISSION DECISION ENGINE (Case Study 20)")
print("=" * 70)

# Input stage: Read applicants
# Format of tuple: (applicant_id, name, math, physics, chemistry, entrance_rank, category, interview)
applicants = []

print("Enter applicant details (or enter '0' at prompt to load standard test set):")
num_input = input("Enter number of applicants to process: ").strip()

if num_input == "" or num_input == "0" or num_input.lower() == "demo":
    print("\n[Loading Predefined Comprehensive Evaluation Dataset (5 Applicants)...]")
    # Pre-configured test dataset covering general, category relaxation, ties, and ineligibility
    applicants.append(("APP101", "Aarav Sharma", 88, 82, 75, 450, "GEN", 22))
    applicants.append(("APP102", "Bhavna Patel", 65, 58, 52, 1200, "OBC", 20))
    applicants.append(("APP103", "Chirag Verma", 92, 78, 75, 450, "GEN", 22)) # Ties with APP101 on composite components
    applicants.append(("APP104", "Deepak Rao", 48, 50, 42, 3500, "SC", 15))   # Fails eligibility
    applicants.append(("APP105", "Divya Nair", 88, 82, 75, 450, "GEN", 22))   # Exact tie with APP101 across criteria
    applicants.append(("APP106", "Esha Reddy", 72, 68, 64, 800, "OBC", 24))
else:
    total_count = int(num_input)
    for i in range(total_count):
        print("\nEntering details for Applicant #" + str(i + 1) + ":")
        app_id = input("  Applicant ID (e.g. APP101): ").strip()
        name = input("  Full Name: ").strip()
        math = float(input("  Mathematics Marks (out of 100): ").strip())
        physics = float(input("  Physics Marks (out of 100): ").strip())
        chem = float(input("  Chemistry Marks (out of 100): ").strip())
        rank = int(input("  Entrance Exam Rank (1 to 10000): ").strip())
        category = input("  Category (GEN / OBC / SC / ST): ").strip().upper()
        interview = float(input("  Interview Score (out of 25): ").strip())
        
        applicant_tuple = (app_id, name, math, physics, chem, rank, category, interview)
        applicants.append(applicant_tuple)

print("\n" + "-" * 70)
print("STAGE 1: ELIGIBILITY VERIFICATION")
print("-" * 70)

# Available Seats Configuration
TOTAL_SEATS = 3
CATEGORY_RESERVED_SEATS = 1

eligible_applicants = []
ineligible_applicants = []

# Verify eligibility using tuple unpacking and multi-criteria conditionals
for app in applicants:
    (app_id, name, m, p, c, rk, cat, intv) = app
    pcm_total = m + p + c
    
    # Determine criteria based on category
    if cat == "GEN":
        min_pcm = 180.0
        min_m = 60.0
        min_p = 55.0
        min_c = 50.0
    else:
        # 10% relaxation for reserved categories
        min_pcm = 162.0
        min_m = 54.0
        min_p = 49.0
        min_c = 45.0
        
    is_eligible = True
    reason = "Meets all cut-offs"
    
    if pcm_total < min_pcm:
        is_eligible = False
        reason = "PCM aggregate " + str(pcm_total) + " below cutoff (" + str(min_pcm) + ")"
    elif m < min_m:
        is_eligible = False
        reason = "Math score " + str(m) + " below cutoff (" + str(min_m) + ")"
    elif p < min_p:
        is_eligible = False
        reason = "Physics score " + str(p) + " below cutoff (" + str(min_p) + ")"
    elif c < min_c:
        is_eligible = False
        reason = "Chemistry score " + str(c) + " below cutoff (" + str(min_c) + ")"
        
    if is_eligible:
        # Calculate Composite Merit Index (CMI)
        # Weightage: 50% PCM Percentage + 30% Normalized Rank + 20% Interview Score scaled to 100
        pcm_pct = pcm_total / 3.0
        norm_rank_score = (10000.0 - rk) / 100.0
        norm_interview = (intv / 25.0) * 100.0
        cmi = (pcm_pct * 0.50) + (norm_rank_score * 0.30) + (norm_interview * 0.20)
        cmi = round(cmi, 2)
        
        # Store enriched tuple: (cmi, math, physics, interview, inv_rank, app_id, name, cat, pcm_total, rk, intv)
        # inv_rank is (10000 - rk) so higher value means better (lower numeric) rank
        eval_tuple = (cmi, m, p, intv, 10000 - rk, app_id, name, cat, pcm_total, rk, intv)
        eligible_applicants.append(eval_tuple)
        print("  [ELIGIBLE]   " + app_id + " - " + name + " (" + cat + ") | PCM: " + str(pcm_total) + " | CMI: " + str(cmi))
    else:
        ineligible_applicants.append((app_id, name, cat, reason))
        print("  [INELIGIBLE] " + app_id + " - " + name + " (" + cat + ") | Reason: " + reason)

print("\n" + "-" * 70)
print("STAGE 2: MULTI-CRITERIA TIE-BREAKING & MERIT RANKING")
print("-" * 70)

# Sort eligible candidates using Bubble Sort (No lambdas, no functions, no custom sort keys)
# Comparison order: CMI desc -> Math desc -> Physics desc -> Interview desc -> Entrance Rank asc
n = len(eligible_applicants)
for i in range(n - 1):
    for j in range(0, n - i - 1):
        cand1 = eligible_applicants[j]
        cand2 = eligible_applicants[j + 1]
        
        # Unpack comparison criteria
        (cmi1, m1, p1, intv1, inv_rk1, id1, name1, cat1, pcm1, rk1, raw_intv1) = cand1
        (cmi2, m2, p2, intv2, inv_rk2, id2, name2, cat2, pcm2, rk2, raw_intv2) = cand2
        
        should_swap = False
        if cmi1 < cmi2:
            should_swap = True
        elif cmi1 == cmi2:
            # Tie-break 1: Mathematics
            if m1 < m2:
                should_swap = True
            elif m1 == m2:
                # Tie-break 2: Physics
                if p1 < p2:
                    should_swap = True
                elif p1 == p2:
                    # Tie-break 3: Interview Score
                    if intv1 < intv2:
                        should_swap = True
                    elif intv1 == intv2:
                        # Tie-break 4: Lower Entrance Rank (Higher inv_rk)
                        if inv_rk1 < inv_rk2:
                            should_swap = True
                            
        if should_swap:
            eligible_applicants[j] = cand2
            eligible_applicants[j + 1] = cand1

print("Merit Ranking after Tie-Breaking:")
rank_num = 1
for cand in eligible_applicants:
    (cmi, m, p, intv, inv_rk, app_id, name, cat, pcm, rk, raw_intv) = cand
    print("  Rank " + str(rank_num) + ": " + app_id + " | " + name + " | Category: " + cat + " | CMI: " + str(cmi) + " [M:" + str(m) + ", P:" + str(p) + ", Rank:" + str(rk) + "]")
    rank_num = rank_num + 1

print("\n" + "-" * 70)
print("STAGE 3: SEAT ALLOCATION (Open Merit & Category Quota)")
print("-" * 70)

open_seats = TOTAL_SEATS - CATEGORY_RESERVED_SEATS
category_seats = CATEGORY_RESERVED_SEATS

final_results = []
allocated_open_count = 0
allocated_category_count = 0

# Allocation Pass 1: Open Category Seats (pure merit)
for cand in eligible_applicants:
    (cmi, m, p, intv, inv_rk, app_id, name, cat, pcm, rk, raw_intv) = cand
    status = "WAITLISTED"
    
    if allocated_open_count < open_seats:
        status = "ADMITTED (Open Merit)"
        allocated_open_count = allocated_open_count + 1
    elif cat != "GEN" and allocated_category_count < category_seats:
        status = "ADMITTED (Category Quota: " + cat + ")"
        allocated_category_count = allocated_category_count + 1
        
    final_results.append((app_id, name, cat, cmi, status))

print("\n" + "=" * 70)
print("FINAL UNIVERSITY ADMISSION DECISION SHEET")
print("=" * 70)
print(f"{'App ID':<8} {'Candidate Name':<18} {'Cat':<6} {'CMI':<8} {'Admission Decision'}")
print("-" * 70)
for res in final_results:
    (app_id, name, cat, cmi, status) = res
    print(f"{app_id:<8} {name:<18} {cat:<6} {cmi:<8.2f} {status}")

for inel in ineligible_applicants:
    (app_id, name, cat, reason) = inel
    print(f"{app_id:<8} {name:<18} {cat:<6} {'N/A':<8} REJECTED ({reason})")

print("=" * 70)
print(f"Total Processed: {len(applicants)} | Eligible: {len(eligible_applicants)} | Ineligible: {len(ineligible_applicants)}")
print(f"Total Admitted: {allocated_open_count + allocated_category_count} / {TOTAL_SEATS} seats")
print("=" * 70)
