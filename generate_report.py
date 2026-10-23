# Script to compile Consolidated_Report.md and Consolidated_Report.html, then invoke headless Chrome/Edge to render Consolidated_Report.pdf
import os
import subprocess

base_dir = r"C:\Users\HP\.gemini\antigravity-ide\scratch\Python-Activity-Based-Learning"

case_studies = [
    ("Case_Study_20", "Case Study 20: University Admission Decision Engine", "Range 1-50"),
    ("Case_Study_26", "Case Study 26: Nested Loop Examination Seating Generator", "Range 1-50"),
    ("Case_Study_35", "Case Study 35: Text Compression Using Character Runs (RLE)", "Range 1-50"),
    ("Case_Study_42", "Case Study 42: Student Marks Matrix Analysis", "Range 1-50"),
    ("Case_Study_56", "Case Study 56: Student Group Formation with Score Balancing", "Range 51-75"),
    ("Case_Study_61", "Case Study 61: Nested List Examination Seating Validation", "Range 51-75"),
    ("Case_Study_75", "Case Study 75: Integrated Student Record Consistency Checker", "Range 51-75"),
    ("Case_Study_85", "Case Study 85: Smart Classroom Timetable Allocation", "Range 76-100"),
    ("Case_Study_88", "Case Study 88: Multi-Branch Retail Inventory Transfer", "Range 76-100"),
    ("Case_Study_100", "Case Study 100: Comprehensive Smart Campus Management Simulation", "Range 76-100")
]

# 1. Compile Consolidated_Report.md
md_lines = []
md_lines.append("# Dr. RVR NRI Institute of Technology")
md_lines.append("## School of Computer Studies")
md_lines.append("### Course: Python Programming - Activity-Based Learning (ABL)")
md_lines.append("\n**Consolidated Assignment Report: 10 Difficult-Level Case Studies**")
md_lines.append("\n---\n")
md_lines.append("### 👨‍🎓 Student & Evaluation Metadata")
md_lines.append("- **Student Name:** [Your Name]")
md_lines.append("- **Roll Number:** [Your Roll Number]")
md_lines.append("- **Academic Level:** 1st Year B.Tech")
md_lines.append("- **Branch & Section:** [e.g., CSE - A]")
md_lines.append("- **Faculty Mentor:** [Faculty Mentor Name]")
md_lines.append("- **Academic Year:** 2026–2027\n")
md_lines.append("---\n")
md_lines.append("## 📑 Table of Contents")
for idx, (folder, title, rng) in enumerate(case_studies):
    md_lines.append(f"{idx+1}. [{title} ({rng})](#{folder.lower()})")
md_lines.append("\n---\n")

html_sections = []

for idx, (folder, title, rng) in enumerate(case_studies):
    doc_path = os.path.join(base_dir, folder, "documentation.md")
    sol_path = os.path.join(base_dir, folder, "solution.py")
    
    with open(doc_path, "r", encoding="utf-8") as f:
        doc_content = f.read()
    with open(sol_path, "r", encoding="utf-8") as f:
        sol_code = f.read()
        
    md_lines.append(f"\n<div id='{folder.lower()}'></div>\n\n# Case Study #{idx+1}: {title}\n")
    # Replace placeholder code in doc with real source code in md
    full_doc = doc_content.replace("# Refer to solution.py in the same directory for complete executable script.", sol_code)
    md_lines.append(full_doc)
    md_lines.append("\n\n---\n")
    
    # Store section for HTML
    html_sections.append((idx + 1, folder, title, rng, full_doc, sol_code))

consolidated_md_path = os.path.join(base_dir, "Consolidated_Report.md")
with open(consolidated_md_path, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

print(f"[SUCCESS] Consolidated_Report.md generated ({len(md_lines)} lines).")

# 2. Compile Consolidated_Report.html with high quality academic printing styles
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Python Programming (ABL) Consolidated Report - Dr. RVR NRI Institute of Technology</title>
<style>
  @page {
    size: A4;
    margin: 20mm 15mm 20mm 15mm;
  }
  body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #1a202c;
    line-height: 1.6;
    margin: 0;
    padding: 20px;
    background-color: #ffffff;
  }
  .cover-page {
    text-align: center;
    padding: 60px 20px;
    border: 3px double #2b6cb0;
    border-radius: 8px;
    margin-bottom: 50px;
    page-break-after: always;
  }
  .inst-title {
    font-size: 26px;
    font-weight: bold;
    color: #1a365d;
    margin-bottom: 5px;
    text-transform: uppercase;
  }
  .dept-title {
    font-size: 18px;
    color: #2b6cb0;
    margin-bottom: 30px;
  }
  .assign-badge {
    display: inline-block;
    background-color: #ebf8ff;
    color: #2b6cb0;
    padding: 8px 18px;
    font-size: 14px;
    font-weight: bold;
    border-radius: 20px;
    border: 1px solid #bee3f8;
    margin-bottom: 25px;
  }
  .report-title {
    font-size: 24px;
    font-weight: 700;
    color: #2d3748;
    margin: 20px 0;
  }
  .meta-box {
    margin: 40px auto;
    max-width: 520px;
    text-align: left;
    border-collapse: collapse;
    width: 100%;
  }
  .meta-box td {
    padding: 10px 14px;
    border: 1px solid #cbd5e0;
  }
  .meta-box td.label {
    background-color: #f7fafc;
    font-weight: 600;
    width: 40%;
  }
  .case-container {
    page-break-before: always;
    margin-top: 30px;
  }
  h1 {
    color: #1a365d;
    font-size: 20px;
    border-bottom: 2px solid #3182ce;
    padding-bottom: 6px;
    margin-top: 25px;
  }
  h2 {
    color: #2b6cb0;
    font-size: 16px;
    margin-top: 18px;
    margin-bottom: 6px;
  }
  pre {
    background-color: #f7fafc;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #3182ce;
    padding: 12px;
    border-radius: 4px;
    font-family: Consolas, 'Courier New', monospace;
    font-size: 12px;
    overflow-x: auto;
    white-space: pre-wrap;
  }
  code {
    font-family: Consolas, 'Courier New', monospace;
    background-color: #edf2f7;
    padding: 2px 5px;
    border-radius: 3px;
    font-size: 12px;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
    font-size: 13px;
  }
  th, td {
    border: 1px solid #cbd5e0;
    padding: 8px 10px;
    text-align: left;
  }
  th {
    background-color: #edf2f7;
    color: #2d3748;
    font-weight: 600;
  }
  .toc-item {
    padding: 6px 0;
    border-bottom: 1px dotted #cbd5e0;
  }
</style>
</head>
<body>

<div class="cover-page">
  <div class="inst-title">Dr. RVR NRI Institute of Technology</div>
  <div class="dept-title">School of Computer Studies</div>
  <div class="assign-badge">ACTIVITY-BASED LEARNING (ABL) ASSIGNMENT</div>
  <div class="report-title">Python Programming: 10 Difficult-Level Case Studies<br><span style="font-size:16px; font-weight:normal; color:#4a5568;">Comprehensive Code, Algorithms, Flowcharts, Test Cases & Analysis</span></div>
  
  <table class="meta-box">
    <tr><td class="label">Student Name</td><td>[Your Name]</td></tr>
    <tr><td class="label">Roll Number</td><td>[Your Roll Number]</td></tr>
    <tr><td class="label">Academic Level</td><td>1st Year B.Tech</td></tr>
    <tr><td class="label">Branch & Section</td><td>[e.g., CSE - A]</td></tr>
    <tr><td class="label">Course Title</td><td>Python Programming (ABL)</td></tr>
    <tr><td class="label">Faculty Mentor</td><td>[Faculty Mentor Name]</td></tr>
    <tr><td class="label">Academic Year</td><td>2026–2027</td></tr>
    <tr><td class="label">GitHub Repository</td><td>Python-Activity-Based-Learning</td></tr>
  </table>

  <p style="margin-top: 40px; font-size: 13px; color: #718096;">
    Strictly adhering to institutional syllabus guidelines: Basic programming constructs, variables, loops, conditionals, 2D nested lists, tuples, and unpacking.
  </p>
</div>

<div style="page-break-after: always; padding: 20px;">
  <h1 style="text-align: center;">Table of Contents</h1>
  <div style="margin-top: 25px;">
"""

for idx, (folder, title, rng) in enumerate(case_studies):
    html_content += f"""
    <div class="toc-item">
      <strong>{idx+1}. {title}</strong> <span style="float:right; color:#718096;">{rng}</span>
    </div>
    """

html_content += """
  </div>
</div>
"""

# Helper to format basic markdown to HTML
def simple_md_to_html(md_text):
    import re
    # Convert code blocks
    def repl_code(m):
        lang = m.group(1) or ""
        code = m.group(2).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f"<pre><code class='{lang}'>{code}</code></pre>"
    
    out = re.sub(r'```([a-zA-Z0-9]*)\n(.*?)```', repl_code, md_text, flags=re.DOTALL)
    
    # Headers
    out = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', out, flags=re.MULTILINE)
    out = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', out, flags=re.MULTILINE)
    
    # Inline backticks
    out = re.sub(r'`([^`]+)`', r'<code>\1</code>', out)
    
    # Bold
    out = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', out)
    
    # Markdown tables
    lines = out.split("\n")
    in_table = False
    new_lines = []
    table_rows = []
    
    for l in lines:
        if "|" in l and not l.strip().startswith("```"):
            parts = [p.strip() for p in l.split("|")[1:-1]]
            if len(parts) > 0 and not all(c in "- :" for c in "".join(parts)):
                table_rows.append(parts)
                in_table = True
            elif all(c in "- :" for c in "".join(parts)):
                continue
        else:
            if in_table:
                # render table
                t_html = ["<table>"]
                for r_i, r in enumerate(table_rows):
                    t_html.append("<tr>")
                    tag = "th" if r_i == 0 else "td"
                    for cell in r:
                        t_html.append(f"<{tag}>{cell}</{tag}>")
                    t_html.append("</tr>")
                t_html.append("</table>")
                new_lines.append("\n".join(t_html))
                table_rows = []
                in_table = False
            new_lines.append(l)
            
    if in_table:
        t_html = ["<table>"]
        for r_i, r in enumerate(table_rows):
            t_html.append("<tr>")
            tag = "th" if r_i == 0 else "td"
            for cell in r:
                t_html.append(f"<{tag}>{cell}</{tag}>")
            t_html.append("</tr>")
        t_html.append("</table>")
        new_lines.append("\n".join(t_html))
        
    return "\n".join(new_lines)

for idx, folder, title, rng, full_doc, sol_code in html_sections:
    body_html = simple_md_to_html(full_doc)
    html_content += f"""
    <div class="case-container">
      <h1>Case Study #{idx}: {title}</h1>
      <p><em>Category Range: {rng} |Dr. RVR NRI Institute of Technology</em></p>
      {body_html}
    </div>
    """

html_content += """
</body>
</html>
"""

consolidated_html_path = os.path.join(base_dir, "Consolidated_Report.html")
with open(consolidated_html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"[SUCCESS] Consolidated_Report.html generated.")

# 3. Invoke Chrome / Edge headless to print PDF
pdf_path = os.path.join(base_dir, "Consolidated_Report.pdf")
chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
if not os.path.exists(chrome_exe):
    chrome_exe = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

cmd = [
    chrome_exe,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path}",
    consolidated_html_path
]

print(f"Executing: {' '.join(cmd)}")
res = subprocess.run(cmd, capture_output=True, text=True)
if os.path.exists(pdf_path):
    size_kb = round(os.path.getsize(pdf_path) / 1024, 2)
    print(f"[SUCCESS] Consolidated_Report.pdf created successfully! Size: {size_kb} KB")
else:
    print(f"[ERROR] PDF generation failed: {res.stderr}")
