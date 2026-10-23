# Case Study 75: Integrated Student Record Consistency Checker
# Allowed Concepts: Variables, Data Types, Operators, Conditionals, Loops, Strings, Lists, Tuples & Unpacking
# Prohibited: Functions, Classes/OOP, Dictionaries, External Libraries (re, pandas)

print("=" * 80)
print("     INTEGRATED STUDENT RECORD CONSISTENCY & VALIDITY CHECKER (Case Study 75)")
print("=" * 80)

mode_input = input("Enter '1' for interactive entry or '0' for Automated Test Dataset: ").strip()

# Raw student records: (roll_number, full_name, email, phone, cgpa_str, branch, dob)
raw_records = []

if mode_input == "" or mode_input == "0" or mode_input.lower() == "demo":
    print("\n[Loading Benchmark Test Database (7 Student Records with Varied Anomalies)...]")
    # Valid Record
    raw_records.append(("26CS01", "Aarav Sharma", "aarav.sharma@nrtec.ac.in", "9876543210", "8.95", "CSE", "15-08-2005"))
    # Inconsistent Case in Name + valid email
    raw_records.append(("26EC02", "bHaVnA pAtEl", "bhavna.patel@gmail.com", "8765432109", "9.20", "ECE", "22-11-2004"))
    # Invalid Phone (<10 digits) + Invalid CGPA (>10)
    raw_records.append(("26CS03", "Chirag Verma", "chirag.verma@college.edu", "98765", "11.50", "CSE", "10-04-2005"))
    # Duplicate Roll Number of first record + Invalid Email (no @)
    raw_records.append(("26CS01", "Aarav S Clone", "aaravclone_gmail.com", "9123456780", "7.40", "CSE", "15-08-2005"))
    # Invalid Roll Number format + Invalid Branch
    raw_records.append(("INVALID_ROLL", "Deepak Rao", "deepak@yahoo.com", "7654321098", "6.80", "BIOTECH", "05-01-2005"))
    # Phone starting with invalid digit '3' + Non-alphabetic Name with symbols
    raw_records.append(("26IT05", "Esha Reddy #123", "esha.reddy@nrtec.ac.in", "3876543210", "8.10", "IT", "18-09-2005"))
    # Valid Record
    raw_records.append(("26CS06", "Farooq Abdullah", "farooq.a@nrtec.ac.in", "+919988776655", "7.85", "CSE", "30-03-2005"))
else:
    n_recs = int(input("Enter number of student registration records to audit: ").strip())
    for i in range(n_recs):
        print(f"\nEntering Record #{i+1}:")
        r_no = input("  Roll Number (e.g. 26CS01): ").strip()
        f_name = input("  Full Name: ").strip()
        em = input("  Email Address: ").strip()
        ph = input("  Phone Number: ").strip()
        cg = input("  CGPA (0.00 to 10.00): ").strip()
        br = input("  Branch Code (e.g. CSE, ECE, IT, MECH, CIVIL): ").strip().upper()
        dob = input("  Date of Birth (DD-MM-YYYY): ").strip()
        raw_records.append((r_no, f_name, em, ph, cg, br, dob))

total_records = len(raw_records)
valid_branches = ["CSE", "ECE", "EEE", "MECH", "CIVIL", "IT", "CS"]

# Tracking lists
seen_rolls = []
clean_records = []      # List of tuples: (roll, formatted_name, email, cleaned_phone, cgpa_float, branch)
flagged_records = []    # List of tuples: (raw_roll, raw_name, [list of error messages])

print("\n" + "-" * 80)
print("STAGE 1: AUDITING FIELD-BY-FIELD CONSISTENCY")
print("-" * 80)

for idx in range(total_records):
    rec = raw_records[idx]
    (roll, name, email, phone, cgpa_str, branch, dob) = rec
    
    error_list = []
    
    # -----------------------------------------------------
    # 1. Roll Number Validation & Duplicate Detection
    # -----------------------------------------------------
    roll_clean = roll.strip().upper()
    # Format check: exactly 6 characters, first 2 digits, next 2 letters, last 2 digits (e.g. 26CS01)
    if len(roll_clean) != 6:
        error_list.append("Roll number length is not 6 characters")
    else:
        part1_ok = roll_clean[0].isdigit() and roll_clean[1].isdigit()
        part2_ok = roll_clean[2].isalpha() and roll_clean[3].isalpha()
        part3_ok = roll_clean[4].isdigit() and roll_clean[5].isdigit()
        if not (part1_ok and part2_ok and part3_ok):
            error_list.append("Roll number violates standard pattern (YYBBSS)")
            
    # Check duplicate roll number
    is_duplicate = False
    for r in seen_rolls:
        if r == roll_clean:
            is_duplicate = True
            break
    if is_duplicate:
        error_list.append("Duplicate roll number detected in cohort")
    else:
        seen_rolls.append(roll_clean)

    # -----------------------------------------------------
    # 2. Full Name Cleaning & Format Standardization
    # -----------------------------------------------------
    name_stripped = name.strip()
    # Check for illegal characters (digits/symbols)
    name_chars_ok = True
    for ch in name_stripped:
        if not (ch.isalpha() or ch == " "):
            name_chars_ok = False
            break
            
    if not name_chars_ok or len(name_stripped) < 2:
        error_list.append("Name contains invalid characters or numbers")
        formatted_name = name_stripped
    else:
        # Standardize to proper Title Case without external functions
        words = name_stripped.split()
        clean_words = []
        for w in words:
            if len(w) > 0:
                capitalized_word = w[0].upper() + w[1:].lower()
                clean_words.append(capitalized_word)
        formatted_name = " ".join(clean_words)

    # -----------------------------------------------------
    # 3. Email Address Consistency
    # -----------------------------------------------------
    email_clean = email.strip()
    at_count = 0
    at_pos = -1
    for char_i in range(len(email_clean)):
        if email_clean[char_i] == "@":
            at_count = at_count + 1
            at_pos = char_i
            
    if at_count != 1 or at_pos == 0 or at_pos == len(email_clean) - 1:
        error_list.append("Email lacks valid '@' structure")
    else:
        # Must contain a period after the @ symbol
        domain_part = email_clean[at_pos + 1:]
        if "." not in domain_part or domain_part.startswith(".") or domain_part.endswith("."):
            error_list.append("Email domain structure invalid (missing dot)")

    # -----------------------------------------------------
    # 4. Phone Number Standardization (10-Digit Mobile)
    # -----------------------------------------------------
    raw_digits = ""
    for ch in phone:
        if ch.isdigit():
            raw_digits = raw_digits + ch
            
    # Handle optional leading +91 or leading 0
    cleaned_phone = ""
    if len(raw_digits) == 12 and raw_digits.startswith("91"):
        cleaned_phone = raw_digits[2:]
    elif len(raw_digits) == 11 and raw_digits.startswith("0"):
        cleaned_phone = raw_digits[1:]
    elif len(raw_digits) == 10:
        cleaned_phone = raw_digits
    else:
        error_list.append(f"Phone must contain 10 digits (found {len(raw_digits)})")
        
    if len(cleaned_phone) == 10:
        # Standard Indian mobile first digit rule: 6, 7, 8, or 9
        if cleaned_phone[0] not in ["6", "7", "8", "9"]:
            error_list.append("Mobile number must start with 6, 7, 8, or 9")

    # -----------------------------------------------------
    # 5. CGPA Range & Data Type Conversion
    # -----------------------------------------------------
    cgpa_val = -1.0
    try:
        cgpa_val = float(cgpa_str)
        if cgpa_val < 0.0 or cgpa_val > 10.0:
            error_list.append(f"CGPA {cgpa_val} outside allowable scale (0.00 - 10.00)")
    except:
        error_list.append("CGPA is not a valid floating-point number")

    # -----------------------------------------------------
    # 6. Academic Branch Validity
    # -----------------------------------------------------
    branch_clean = branch.strip().upper()
    branch_ok = False
    for vb in valid_branches:
        if branch_clean == vb:
            branch_ok = True
            break
    if not branch_ok:
        error_list.append(f"Branch '{branch_clean}' is not an authorized academic program")

    # Final Classification
    if len(error_list) == 0:
        clean_records.append((roll_clean, formatted_name, email_clean, cleaned_phone, cgpa_val, branch_clean))
        print(f"  [CONSISTENT]  {roll_clean:<8} | {formatted_name:<20} | Verified")
    else:
        flagged_records.append((roll, name, error_list))
        print(f"  [FLAGGED]     {roll:<8} | {name:<20} | Errors: {len(error_list)}")

# ---------------------------------------------------------
# STAGE 2: REPORT GENERATION
# ---------------------------------------------------------
print("\n" + "=" * 80)
print("VERIFIED CLEAN & STANDARDIZED STUDENT DATABASE")
print("=" * 80)
print(f"{'Roll No':<8} {'Standardized Full Name':<22} {'Branch':<8} {'CGPA':<6} {'Mobile':<12} {'Email'}")
print("-" * 80)
for cln in clean_records:
    (r_no, f_nm, em, ph, cg, br) = cln
    print(f"{r_no:<8} {f_nm:<22} {br:<8} {cg:<6.2f} {ph:<12} {em}")

print("\n" + "=" * 80)
print("INCONSISTENCY AUDIT LOG: FLAGGED REGISTRATION RECORDS")
print("=" * 80)
for flg in flagged_records:
    (raw_r, raw_n, errs) = flg
    print(f"\nStudent: {raw_n} (Roll: {raw_r})")
    for e in errs:
        print(f"  [ERROR] {e}")

# Database Health Metrics
valid_count = len(clean_records)
flawed_count = len(flagged_records)
health_score = round((valid_count / total_records) * 100, 2)

print("\n" + "=" * 80)
print("STUDENT RECORD DATABASE HEALTH SCORECARD")
print("=" * 80)
print(f"Total Student Ingestion Records : {total_records}")
print(f"Passed All Consistency Checks  : {valid_count}")
print(f"Flagged Inconsistent Records   : {flawed_count}")
print(f"Data Health / Quality Index     : {health_score}%")
if health_score >= 80.0:
    print("Database Quality Status         : [HIGH INTEGRITY]")
else:
    print("Database Quality Status         : [DATA SANITIZATION & CORRECTION REQUIRED]")
print("=" * 80)
