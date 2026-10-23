# Case Study 26: Nested Loop Examination Seating Generator

## 1. Problem Statement
Educational institutions require robust anti-malpractice seating arrangements for mid-semester and end-semester examinations. When students from two differing departments (e.g., Computer Science and Electronics Engineering) share an examination hall of dimension $R \times C$, no two students from the same department may be seated adjacent to one another horizontally or vertically. Additionally, damaged or reserved desks must be accounted for without disrupting the alternating pattern. The system must validate capacity, generate a 2D seating matrix using nested loops, and run an automated adjacency audit to guarantee compliance.

---

## 2. Objectives
- Model an $R \times C$ examination hall as a dynamic 2D nested list (matrix).
- Validate total student counts against total and usable desk capacity.
- Implement nested loop matrix traversal adhering to a parity-based alternation rule: $(r + c) \pmod 2$.
- Gracefully bypass blocked/reserved desks while handling uneven class sizes with `[EMPTY]` indicators.
- Execute an adjacency audit checking all cardinal neighbors (horizontal and vertical) to verify zero same-department adjacency.
- Adhere strictly to allowed syllabus constructs: variables, nested loops, conditional statements, nested lists, and string slicing.

---

## 3. Assumptions
- Hall dimensions $R$ (rows) and $C$ (columns) are positive integers.
- Two student cohorts are provided as lists of roll number strings (e.g., `CS101`, `EC201`), where the first two letters denote the department identifier.
- Alternation rule: Cells where $(row + col) \equiv 0 \pmod 2$ are allocated to Department A; cells where $(row + col) \equiv 1 \pmod 2$ are allocated to Department B.
- Blocked desks are represented as a list of coordinate tuples: `(row_index, col_index)`.
- If candidates in a cohort are exhausted before available alternating slots, remaining slots are labeled `[EMPTY]`.

---

## 4. Algorithm
- **Step 1:** Read hall dimensions ($R$, $C$), student cohorts for Department A and Department B, and list of blocked coordinates.
- **Step 2:** Compute $Total\_Capacity = R \times C$ and $Usable\_Capacity = Total\_Capacity - len(blocked\_seats)$.
- **Step 3:** Validate whether $(len(students\_a) + len(students\_b)) \le Usable\_Capacity$. If false, display capacity error.
- **Step 4:** Initialize an empty 2D matrix of dimensions $R \times C$ populated with placeholder strings.
- **Step 5:** Traverse `blocked_seats` and update matrix cells at coordinates $(r, c)$ to `[BLOCKED]`.
- **Step 6:** Initialize index pointers $idx\_a = 0$ and $idx\_b = 0$.
- **Step 7:** Using nested loops for row $r \in [0, R-1]$ and column $c \in [0, C-1]$:
  - If cell $(r, c)$ is `[BLOCKED]`, skip to the next iteration.
  - If $(r + c) \pmod 2 == 0$:
    - If $idx\_a < len(students\_a)$, place $students\_a[idx\_a]$ and increment $idx\_a$.
    - Else, assign `[EMPTY]`.
  - Else:
    - If $idx\_b < len(students\_b)$, place $students\_b[idx\_b]$ and increment $idx\_b$.
    - Else, assign `[EMPTY]`.
- **Step 8:** Traverse the generated matrix with nested loops to audit adjacency:
  - For each non-empty, non-blocked cell $(r, c)$, compare department prefix with right neighbor $(r, c+1)$ and down neighbor $(r+1, c)$.
  - Record any violation where adjacent department prefixes match.
- **Step 9:** Render formatted 2D seating grid with row/column headers and report summary seating density metrics.

---

## 5. Flowchart
```mermaid
flowchart TD
    Start([Start]) --> Init[Read Hall Dimensions R, C and Student Lists A & B]
    Init --> CheckCap{Total Students <= Usable Capacity?}
    CheckCap -- No --> ErrMsg[/Display Capacity Exceeded Warning/] --> End([End])
    CheckCap -- Yes --> AllocMatrix[Initialize R x C 2D List with Default Values]
    AllocMatrix --> MarkBlocked[Mark Coordinates in Blocked List as BLOCKED]
    MarkBlocked --> OuterLoop[Outer Loop: r from 0 to R-1]
    OuterLoop --> InnerLoop[Inner Loop: c from 0 to C-1]
    InnerLoop --> IsBlocked{Seat is BLOCKED?}
    IsBlocked -- Yes --> NextCell[Continue to Next Cell]
    IsBlocked -- No --> ParityCheck{(r + c) % 2 == 0?}
    ParityCheck -- Yes --> AvailA{idx_a < len(A)?}
    AvailA -- Yes --> AssignA[Assign A Student and idx_a++]
    AvailA -- No --> AssignEmptyA[Assign EMPTY]
    ParityCheck -- No --> AvailB{idx_b < len(B)?}
    AvailB -- Yes --> AssignB[Assign B Student and idx_b++]
    AvailB -- No --> AssignEmptyB[Assign EMPTY]
    AssignA --> NextCell
    AssignEmptyA --> NextCell
    AssignB --> NextCell
    AssignEmptyB --> NextCell
    NextCell --> InnerLoop
    InnerLoop -- Complete --> OuterLoop
    OuterLoop -- Complete --> AuditAdjacency[Run Adjacency Audit Loop: Check Right & Down Neighbors]
    AuditAdjacency --> PrintGrid[/Print Formatted 2D Seating Grid & Metrics/]
    PrintGrid --> End
```

---

## 6. Pseudocode
```text
BEGIN NestedLoopSeatingGenerator
    READ rows, cols
    READ students_a, students_b
    READ blocked_seats

    total_capacity = rows * cols
    usable_capacity = total_capacity - LENGTH(blocked_seats)
    total_students = LENGTH(students_a) + LENGTH(students_b)

    IF total_students > usable_capacity THEN
        PRINT "Capacity Exceeded"
    END IF

    // Initialize 2D Matrix
    seating_matrix = []
    FOR r FROM 0 TO rows - 1:
        row_list = []
        FOR c FROM 0 TO cols - 1:
            APPEND "---" TO row_list
        END FOR
        APPEND row_list TO seating_matrix
    END FOR

    FOR EACH (br, bc) IN blocked_seats:
        seating_matrix[br][bc] = "[BLOCKED]"
    END FOR

    idx_a = 0
    idx_b = 0

    FOR r FROM 0 TO rows - 1:
        FOR c FROM 0 TO cols - 1:
            IF seating_matrix[r][c] == "[BLOCKED]" THEN
                CONTINUE
            END IF

            IF (r + c) MOD 2 == 0 THEN
                IF idx_a < LENGTH(students_a) THEN
                    seating_matrix[r][c] = students_a[idx_a]
                    idx_a = idx_a + 1
                ELSE
                    seating_matrix[r][c] = "[EMPTY]"
                END IF
            ELSE
                IF idx_b < LENGTH(students_b) THEN
                    seating_matrix[r][c] = students_b[idx_b]
                    idx_b = idx_b + 1
                ELSE
                    seating_matrix[r][c] = "[EMPTY]"
                END IF
            END IF
        END FOR
    END FOR

    // Adjacency Verification
    violations = 0
    FOR r FROM 0 TO rows - 1:
        FOR c FROM 0 TO cols - 1:
            seat = seating_matrix[r][c]
            IF seat != "[EMPTY]" AND seat != "[BLOCKED]" THEN
                // Check right neighbor
                IF c + 1 < cols THEN
                    IF seat[0:2] == seating_matrix[r][c+1][0:2] THEN
                        violations = violations + 1
                    END IF
                END IF
                // Check down neighbor
                IF r + 1 < rows THEN
                    IF seat[0:2] == seating_matrix[r+1][c][0:2] THEN
                        violations = violations + 1
                    END IF
                END IF
            END IF
        END FOR
    END FOR

    PRINT seating_matrix
    PRINT metrics
END
```

---

## 7. Python Source Code
*Strictly adhering to syllabus constraints: loops, conditionals, 2D nested lists, and string operations.*

```python
# Refer to solution.py in the same directory for complete executable script.
```

---

## 8. Test Cases

### Test Case 1: Standard Examination Grid with Blocked Seats
- **Inputs:**
  - Dimensions: $5 \text{ Rows} \times 6 \text{ Columns}$ ($30$ total seats).
  - Blocked Seats: $(1, 2)$ and $(3, 4)$ ($2$ blocked, $28$ usable).
  - Cohort A (CSE): 13 Students (`CS101` to `CS113`).
  - Cohort B (ECE): 12 Students (`EC201` to `EC212`).
- **Expected Outcome:**
  - All 25 candidates successfully assigned.
  - Alternating checkerboard pattern verified across all active desks.
  - Exactly 3 remaining usable desks marked `[EMPTY]`.
  - Zero adjacency violations.

### Test Case 2: Unequal Cohort Exhaustion Handling
- **Inputs:**
  - Dimensions: $3 \text{ Rows} \times 4 \text{ Columns}$ ($12$ seats).
  - Cohort A (CSE): 6 Students (`CS01` to `CS06`).
  - Cohort B (ECE): 2 Students (`EC01`, `EC02`).
- **Expected Outcome:**
  - Dept B is exhausted after 2 allocations.
  - Odd parity cells subsequently convert safely to `[EMPTY]`.
  - Zero consecutive Dept A students placed horizontally or vertically.

---

## 9. Output & Execution Log
```text
======================================================================
     EXAMINATION SEATING MATRIX GENERATOR (Case Study 26)
======================================================================
Enter '1' for Interactive Input or '0' for Automated Test Dataset: 0
[Loading Standard Test Configuration: 5 Rows x 6 Columns (Capacity: 30)]

----------------------------------------------------------------------
STAGE 1: CAPACITY & ALTERNATION VALIDATION
----------------------------------------------------------------------
Total Hall Seats     : 30
Blocked/Broken Seats : 2
Usable Seats         : 28
Total Candidates     : 25 (CSE: 13, ECE: 12)

[VALIDATION SUCCESS] Hall capacity is sufficient.

----------------------------------------------------------------------
STAGE 2: GENERATED EXAMINATION SEATING GRID
----------------------------------------------------------------------
        Col 0      Col 1      Col 2      Col 3      Col 4      Col 5      
        ------------------------------------------------------------
Row 0   | CS101     EC201     CS102     EC202     CS103     EC203     
Row 1   | EC204     CS104     [BLOCKED] CS105     EC205     CS106     
Row 2   | CS107     EC206     CS108     EC207     CS109     EC208     
Row 3   | EC209     CS110     EC210     CS111     [BLOCKED] CS112     
Row 4   | CS113     EC211     [EMPTY]   EC212     [EMPTY]   [EMPTY]   
----------------------------------------------------------------------

----------------------------------------------------------------------
STAGE 3: ADJACENCY & MALPRACTICE AUDIT
----------------------------------------------------------------------
  [AUDIT PASSED] Zero adjacency violations detected. Anti-cheating alternating constraint verified!

======================================================================
EXAMINATION SEATING SUMMARY METRICS
======================================================================
Total Hall Dimensions : 5 Rows x 6 Columns
Total Seat Capacity   : 30
Blocked Seats         : 2
CSE Seated       : 13 / 13 (Unseated: 0)
ECE Seated       : 12 / 12 (Unseated: 0)
Empty Desks Remaining : 3
Usable Seat Density   : 89.29%
======================================================================
```

---

## 10. Conclusion
Case Study 26 showcases 2D matrix manipulation and nested loop control in Python. By mathematically coupling cell coordinates to parity-based alternating allocation, the algorithm guarantees strict separation of examination cohorts while dynamically accommodating hardware faults (blocked seats) and unequal cohort distributions.
