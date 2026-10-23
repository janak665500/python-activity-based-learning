# Case Study 61: Nested List Examination Seating Validation

## 1. Problem Statement
Before administering examinations, university exam controllers must rigorously audit proposed room seating plans. Unlike generator systems that build plans from scratch, an integrity validator must inspect an existing $R \times C$ seating plan to identify human error, administrative slip-ups, and anti-cheating infringements. Specifically, the validator must detect: (1) duplicate seat assignments for the same roll number, (2) unauthorized student allocations to physically damaged or reserved desks, (3) empty desk tracking, and (4) branch adjacency violations where students from the same department sit directly next to each other horizontally or vertically.

---

## 2. Objectives
- Traverse and inspect a 2D nested list representation of an examination hall grid.
- Implement duplicate detection across all allocated cells without using forbidden `set` data structures or dictionaries.
- Validate cell coordinates against an official designated list of reserved/damaged desk coordinate tuples.
- Perform orthogonal neighbor checking (horizontal and vertical adjacency) to audit adherence to inter-branch separation.
- Generate an audit discrepancy log specifying exact coordinates and issue descriptions, followed by a binary compliance verdict (`PASSED` / `FAILED`).
- Strictly adhere to 1st-year B.Tech syllabus guidelines: variables, conditionals, loops, nested lists, parallel tracking lists, and tuples.

---

## 3. Assumptions
- The hall seating plan is stored as a 2D nested list of dimensions $R \times C$.
- Desks may contain:
  - Valid student roll number strings (e.g., `CS101`, `EC202`).
  - Empty desk placeholders: `[EMPTY]`, `EMPTY`, or `---`.
  - Legitimate reserved seat placeholders: `[RESERVED]`, `RESERVED`, or `[BLOCKED]`.
- The first two letters of any active roll number identify the student's academic branch (e.g., `CS`, `EC`).
- Reserved/damaged desks are defined by coordinate tuples `(row_index, col_index)`.

---

## 4. Algorithm
- **Step 1:** Read the examination hall dimensions $R$ and $C$, the official `reserved_coords` list of tuples, and the $R \times C$ 2D seating matrix `hall_grid`.
- **Step 2:** Initialize tracking structures:
  - `seen_students = []`, `seen_positions = []` for linear duplicate tracking.
  - `duplicate_errors = []`, `reserved_violations = []`, `adjacency_violations = []`.
  - Counters: `occupied_count = 0`, `empty_count = 0`.
- **Step 3 (Single-Cell Inspection Loop):** Iterate through each row $r \in [0, R-1]$ and column $c \in [0, C-1]$:
  - If cell is empty (`[EMPTY]`), increment `empty_count` and continue.
  - If cell is legitimate reserved placeholder (`[RESERVED]`), continue.
  - Otherwise, increment `occupied_count`.
  - **Check Reserved Desk:** If $(r, c)$ exists in `reserved_coords`, record violation in `reserved_violations`.
  - **Check Duplicate Allocation:** Search `seen_students`. If current roll number is already present, record tuple `(roll, original_pos, current_pos)` in `duplicate_errors`. Else, append roll and position to tracking lists.
- **Step 4 (Adjacency Inspection Loop):** Iterate through non-empty, non-reserved cells:
  - Extract branch prefix (first 2 characters).
  - Compare with right neighbor $(r, c+1)$ if $c + 1 < C$. If right neighbor has matching branch prefix, record horizontal violation.
  - Compare with down neighbor $(r+1, c)$ if $r + 1 < R$. If down neighbor has matching branch prefix, record vertical violation.
- **Step 5 (Audit Summary):** Sum all errors. If `total_errors == 0`, output `[PASSED - AUDIT APPROVED]`; otherwise, output `[FAILED - REMEDIATION REQUIRED]` with itemized findings.

---

## 5. Flowchart
```mermaid
flowchart TD
    Start([Start]) --> LoadGrid[/Read R x C Seating Grid & Reserved Coordinates/]
    LoadGrid --> DisplayGrid[/Print Input Seating Matrix/]
    DisplayGrid --> CellLoop{For each cell r, c in grid?}
    CellLoop -- Yes --> IsEmpty{Cell is EMPTY?}
    IsEmpty -- Yes --> IncEmpty[empty_count++] --> CellLoop
    IsEmpty -- No --> IsReservedText{Cell is [RESERVED] text?}
    IsReservedText -- Yes --> CellLoop
    IsReservedText -- No --> CheckReservedDesk{(r, c) in reserved_coords?}
    CheckReservedDesk -- Yes --> LogResViolation[Record Reserved Violation]
    CheckReservedDesk -- No --> CheckDup{Roll already in seen_students?}
    LogResViolation --> CheckDup
    CheckDup -- Yes --> LogDupViolation[Record Duplicate Violation] --> CellLoop
    CheckDup -- No --> AddSeen[Add to seen_students & seen_positions] --> CellLoop
    CellLoop -- No --> AdjLoop{For each cell r, c: Check Right & Down Neighbors?}
    AdjLoop -- Yes --> CheckPrefix{Same branch prefix as neighbor?}
    CheckPrefix -- Yes --> LogAdjViolation[Record Adjacency Violation] --> AdjLoop
    CheckPrefix -- No --> AdjLoop
    AdjLoop -- No --> TallyErrors[Count Total Anomalies]
    TallyErrors --> PrintAudit[/Print Itemized Discrepancy Log & Verdict/]
    PrintAudit --> End([End])
```

---

## 6. Pseudocode
```text
BEGIN SeatingPlanValidator
    READ rows, cols, hall_grid, reserved_coords

    seen_students = []
    seen_positions = []
    duplicate_errors = []
    reserved_violations = []
    adjacency_violations = []

    FOR r FROM 0 TO rows - 1:
        FOR c FROM 0 TO cols - 1:
            val = hall_grid[r][c]
            IF val == "[EMPTY]" THEN
                empty_count = empty_count + 1
                CONTINUE
            END IF
            IF val == "[RESERVED]" THEN CONTINUE

            // Reserved violation check
            FOR EACH (rr, rc) IN reserved_coords:
                IF r == rr AND c == rc THEN
                    APPEND (r, c, val) TO reserved_violations
                END IF
            END FOR

            // Duplicate student check
            found = FALSE
            FOR k FROM 0 TO LENGTH(seen_students) - 1:
                IF seen_students[k] == val THEN
                    found = TRUE
                    orig_pos = seen_positions[k]
                    BREAK
                END IF
            END FOR

            IF found THEN
                APPEND (val, orig_pos, (r, c)) TO duplicate_errors
            ELSE
                APPEND val TO seen_students
                APPEND (r, c) TO seen_positions
            END IF
        END FOR
    END FOR

    // Adjacency check
    FOR r FROM 0 TO rows - 1:
        FOR c FROM 0 TO cols - 1:
            val = hall_grid[r][c]
            IF val is active student THEN
                IF c + 1 < cols AND hall_grid[r][c+1] has same branch THEN
                    APPEND horizontal violation
                END IF
                IF r + 1 < rows AND hall_grid[r+1][c] has same branch THEN
                    APPEND vertical violation
                END IF
            END IF
        END FOR
    END FOR

    total_errors = LENGTH(duplicate_errors) + LENGTH(reserved_violations) + LENGTH(adjacency_violations)
    PRINT audit findings and final verdict
END
```

---

## 7. Python Source Code
*Strictly adhering to syllabus constraints: loops, conditionals, 2D nested lists, parallel lists, and tuples.*

```python
# Refer to solution.py in the same directory for complete executable script.
```

---

## 8. Test Cases

### Test Case 1: Duplicate Roll Number Allocation
- **Injected Condition:** Roll number `CS102` placed at Seat $(0, 2)$ and Seat $(3, 1)$.
- **Expected Audit Finding:** Flagged as duplicate allocation showing both coordinate instances.

### Test Case 2: Unauthorized Seating on Reserved/Damaged Desk
- **Injected Condition:** Seat $(1, 1)$ designated in `reserved_coords`, but occupied by `EC205`.
- **Expected Audit Finding:** Flagged as unauthorized occupancy on reserved desk $(1, 1)$.

### Test Case 3: Anti-Cheating Adjacent Branch Infringement
- **Injected Condition:** Two CSE students `CS101` and `CS104` seated side-by-side at $(0, 0)$ and $(0, 1)$.
- **Expected Audit Finding:** Horizontal Adjacency violation flagged at coordinates $(0, 0)$ and $(0, 1)$.

---

## 9. Output & Execution Log
```text
===========================================================================
     EXAMINATION SEATING MATRIX INTEGRITY AUDITOR (Case Study 61)
===========================================================================
Enter '1' for interactive entry or '0' for Automated Test Dataset: 0
[Loading Benchmark Audit Hall Layout: 4 Rows x 5 Columns with Injected Test Anomalies]

---------------------------------------------------------------------------
STAGE 1: VISUALIZING INPUT SEATING PLAN MATRIX
---------------------------------------------------------------------------
       Col 0        Col 1        Col 2        Col 3        Col 4        
       ------------------------------------------------------------
Row 0  | CS101       CS104       CS102       EC201       CS103       
Row 1  | EC202       EC205       CS105       EC203       CS106       
Row 2  | CS107       EC204       CS108       [RESERVED]  EC206       
Row 3  | EC207       CS102       [EMPTY]     EC208       [EMPTY]     

===========================================================================
STAGE 2: DETAILED ANOMALY & MALPRACTICE AUDIT FINDINGS
===========================================================================

[ALERT: DUPLICATE ALLOCATIONS DETECTED (1)]
  - Roll No 'CS102' allocated multiple times: Seat (0, 2) and Seat (3, 1)

[ALERT: RESERVED/DAMAGED DESK VIOLATIONS (1)]
  - Unauthorized student 'EC205' placed on reserved/damaged desk at Row 1, Col 1

[ALERT: BRANCH ADJACENCY (MALPRACTICE RISK) VIOLATIONS (8)]
  - Horizontal Adjacency: 'CS101' at (0,0) next to 'CS104' at (0,1) [Both Branch 'CS']
  - Horizontal Adjacency: 'CS104' at (0,1) next to 'CS102' at (0,2) [Both Branch 'CS']
  - Vertical Adjacency: 'CS102' at (0,2) next to 'CS105' at (1,2) [Both Branch 'CS']
  - Vertical Adjacency: 'EC201' at (0,3) next to 'EC203' at (1,3) [Both Branch 'EC']
  - Vertical Adjacency: 'CS103' at (0,4) next to 'CS106' at (1,4) [Both Branch 'CS']
  - Horizontal Adjacency: 'EC202' at (1,0) next to 'EC205' at (1,1) [Both Branch 'EC']
  - Vertical Adjacency: 'EC205' at (1,1) next to 'EC204' at (2,1) [Both Branch 'EC']
  - Vertical Adjacency: 'CS105' at (1,2) next to 'CS108' at (2,2) [Both Branch 'CS']

===========================================================================
STAGE 3: FINAL EXAMINATION HALL AUDIT VERDICT
===========================================================================
Hall Dimensions        : 4 Rows x 5 Columns (Capacity: 20)
Total Occupied Desks   : 17
Total Empty Desks      : 2
Official Reserved Desks: 2
Total Discrepancies    : 10

AUDIT VERDICT: [FAILED - 10 CRITICAL ISSUES REQUIRE IMMEDIATE REMEDIATION]
===========================================================================
```

---

## 10. Conclusion
Case Study 61 provides practical experience with 2D matrix inspection algorithms. By replacing advanced set structures with linear list scanning and multi-directional index probing, the program demonstrates how low-level algorithmic logic can solve mission-critical administrative compliance problems in educational institutions.
