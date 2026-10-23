# Case Study 35: Text Compression Using Character Runs (Run-Length Encoding)
# Allowed Concepts: Variables, Data Types, Operators, Conditionals, Loops, Strings, Lists, Tuples & Unpacking
# Prohibited: Functions, Classes/OOP, Dictionaries, External Libraries (re, itertools, pandas)

print("=" * 70)
print("     TEXT COMPRESSION & RUN-LENGTH ENCODING ENGINE (Case Study 35)")
print("=" * 70)

mode_input = input("Enter '1' to input custom text or '0' for Automated Test Dataset: ").strip()

test_strings = []
if mode_input == "" or mode_input == "0" or mode_input.lower() == "demo":
    print("\n[Loading Standard Benchmark Test Suite (4 Test Corpora)...]")
    test_strings.append("WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWEEEEEEEEEEEE") # Highly repetitive
    test_strings.append("AAAAABBBCCDAAEEEEEEE")                                                  # Mixed runs
    test_strings.append("XYZABCDEFGHIJKLMNOPQRSTUVWXYZ")                                      # Non-repetitive worst case
    test_strings.append("MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM")                                # Multi-digit run (>30 chars)
else:
    user_str = input("Enter text string to compress (letters/digits): ").strip()
    test_strings.append(user_str)

case_num = 1
for raw_text in test_strings:
    print("\n" + "=" * 70)
    print("ANALYSIS OF CORPUS #" + str(case_num) + ": \"" + (raw_text if len(raw_text) <= 40 else raw_text[:37] + "...") + "\"")
    print("=" * 70)
    
    orig_length = len(raw_text)
    if orig_length == 0:
        print("[WARNING] Empty input string. Skipping.")
        case_num = case_num + 1
        continue
        
    # ----------------------------------------------------
    # STAGE 1: RUN-LENGTH ENCODING (COMPRESSION)
    # ----------------------------------------------------
    compressed_str = ""
    run_records = [] # List of tuples: (char, run_length)
    
    current_char = raw_text[0]
    run_count = 1
    
    # Traverse string sequentially from index 1 to end
    for idx in range(1, orig_length):
        char = raw_text[idx]
        if char == current_char:
            run_count = run_count + 1
        else:
            # Store completed run
            run_records.append((current_char, run_count))
            compressed_str = compressed_str + str(run_count) + current_char
            current_char = char
            run_count = 1
            
    # Record the final character run
    run_records.append((current_char, run_count))
    compressed_str = compressed_str + str(run_count) + current_char
    
    comp_length = len(compressed_str)
    
    print("\nSTAGE 1: COMPRESSION RESULT")
    print("-" * 50)
    print("Original Text   : " + raw_text)
    print("Compressed Text : " + compressed_str)
    print("Original Size   : " + str(orig_length) + " characters")
    print("Compressed Size : " + str(comp_length) + " characters")
    
    # ----------------------------------------------------
    # STAGE 2: RUN-LENGTH DECODING (DECOMPRESSION & INTEGRITY AUDIT)
    # ----------------------------------------------------
    decompressed_str = ""
    digit_buffer = ""
    
    # Sequential traversal with numerical parsing
    for char in compressed_str:
        if "0" <= char <= "9":
            digit_buffer = digit_buffer + char
        else:
            repeat_count = int(digit_buffer)
            # String multiplication construct
            decompressed_str = decompressed_str + (char * repeat_count)
            digit_buffer = ""
            
    print("\nSTAGE 2: DECOMPRESSION & RECONSTRUCTION")
    print("-" * 50)
    print("Decompressed    : " + decompressed_str)
    
    # Integrity check
    if decompressed_str == raw_text:
        print("Integrity Audit : [PASSED] Perfect lossless reconstruction confirmed!")
    else:
        print("Integrity Audit : [FAILED] Decompressed output mismatch!")
        
    # ----------------------------------------------------
    # STAGE 3: RUN DISTRIBUTION & COMPRESSION ANALYTICS
    # ----------------------------------------------------
    total_runs = len(run_records)
    min_run = run_records[0][1]
    max_run = run_records[0][1]
    total_run_chars = 0
    
    for record in run_records:
        (ch, rlen) = record
        if rlen < min_run:
            min_run = rlen
        if rlen > max_run:
            max_run = rlen
        total_run_chars = total_run_chars + rlen
        
    avg_run = round(total_run_chars / total_runs, 2)
    
    # Metrics
    compression_ratio = round((comp_length / orig_length) * 100, 2)
    space_savings = round(((orig_length - comp_length) / orig_length) * 100, 2)
    
    print("\nSTAGE 3: STATISTICAL METRICS & EFFICIENCY")
    print("-" * 50)
    print("Total Unique Character Runs : " + str(total_runs))
    print("Minimum Run Length          : " + str(min_run))
    print("Maximum Run Length          : " + str(max_run))
    print("Average Run Length          : " + str(avg_run))
    print("Compression Ratio           : " + str(compression_ratio) + "%")
    print("Space Savings               : " + str(space_savings) + "%")
    
    if comp_length < orig_length:
        print("Economic Viability          : [BENEFICIAL] Reduced storage by " + str(orig_length - comp_length) + " characters.")
    elif comp_length == orig_length:
        print("Economic Viability          : [NEUTRAL] No size change.")
    else:
        print("Economic Viability          : [INFLATION / NEGATIVE] Run overhead increased size by " + str(comp_length - orig_length) + " characters (Worst-case RLE).")
        
    case_num = case_num + 1

print("\n" + "=" * 70)
print("BENCHMARK SUITE COMPLETED SUCCESSFULLY")
print("=" * 70)
