"""
Generates 3,000 100% Genuine-Looking Google Form Survey Responses
Matching the exact Google Form:
https://docs.google.com/forms/d/e/1FAIpQLSc4YrNID_Pw5o5DnUG3EXrb51bZVFHCJMQi0tSu0ha4CNpStw/viewform

Fixes all Excel UTF-8 BOM encoding issues (preventing â‚¹ and â€“ mojibake)
and outputs both Google Forms export format and clean analytical research format.
"""

import os
import sys
import random
import datetime
import zipfile
import xml.sax.saxutils as saxutils
import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

np.random.seed(42)
random.seed(42)

NUM_RESPONSES = 3000

# Exact options from the Google Form
Q1_OPTIONS = ['Daily', 'Several times a week', 'Once a week', 'A few times a month', 'Rarely']
Q2_OPTIONS = ['Below ₹5,000', '₹5,000–₹10,000', '₹10,001–₹20,000', '₹20,001–₹30,000', 'Above ₹30,000']
Q3_OPTIONS = ['Less than ₹500', '₹500–₹1,000', '₹1,001–₹2,000', '₹2,001–₹5,000', 'More than ₹5,000']
Q4_OPTIONS = ['Yes', 'No', 'Maybe']
Q5_OPTIONS = ['Never', 'Rarely', 'Sometimes', 'Often', 'Very often']
Q6_OPTIONS = ['Never', 'Rarely', 'Sometimes', 'Often', 'Very often']
Q7_OPTIONS = ['Yes, regularly', 'Sometimes', 'Rarely', 'Never']
Q8_OPTIONS = ['Never', 'Rarely', 'Sometimes', 'Often', 'Very often']
Q9_OPTIONS = ['Yes', 'No', 'Not sure']
Q10_OPTIONS = ['Yes', 'No', 'Not sure']
Q11_OPTIONS = ['Never', 'Rarely', 'Sometimes', 'Often', 'Very often']
Q12_OPTIONS = ['Below ₹5,000', '₹5,000–₹10,000', '₹10,001–₹20,000', '₹20,001–₹30,000', 'Above ₹30,000', 'Not applicable / Cannot remember']
Q13_OPTIONS = ['Below ₹5,000', '₹5,000–₹10,000', '₹10,001–₹20,000', '₹20,001–₹30,000', 'Above ₹30,000']
Q15_OPTIONS = ['Yes', 'No', 'Maybe']

# Exact Google Form Question Column Names
GF_COL_TIMESTAMP = "Timestamp"
GF_COL_Q1 = "1. How frequently do you use UPI?"
GF_COL_Q2 = "2. What is your average monthly spending through UPI?"
GF_COL_Q3 = "3. How much cash do you normally carry?"
GF_COL_Q4 = "4. Do you feel you spend more when paying through UPI than cash?"
GF_COL_Q5 = "5. How often do you make unplanned purchases using UPI?"
GF_COL_Q6 = "6. How often do cashback/discounts make you purchase something?"
GF_COL_Q7 = "7. Do you check your UPI transaction history regularly?"
GF_COL_Q8 = "8. Have you ever regretted a purchase made through UPI?"
GF_COL_Q9 = "9. Do you find UPI payments less painful/noticeable than paying cash?"
GF_COL_Q10 = "10. Has your spending increased since you started using UPI regularly?"
GF_COL_Q11 = "11. How often do you make small-value purchases because UPI is convenient?"
GF_COL_Q12 = "12. Approximate monthly spending before using UPI."
GF_COL_Q13 = "13. Approximate monthly spending after regularly using UPI."
GF_COL_Q14 = "14. Rate how much UPI influences your spending behaviour (1–10)."
GF_COL_Q15 = "15. Do you think UPI causes you to overspend?"

# Generate natural submission timestamps over 45 days survey period
# with realistic peaks during college hours (10:00 - 22:30)
start_date = datetime.datetime(2024, 2, 1, 9, 15, 0)
timestamps = []
current_time = start_date

for _ in range(NUM_RESPONSES):
    # Survey bursts: intervals from 30 seconds to 25 minutes during active hours
    # occasionally skip night hours (23:30 to 07:30)
    gap_minutes = random.choices(
        [random.uniform(0.5, 5.0), random.uniform(5.0, 20.0), random.uniform(20.0, 60.0)],
        weights=[0.60, 0.30, 0.10]
    )[0]
    current_time += datetime.timedelta(minutes=gap_minutes)
    
    # If time falls into sleeping hours (midnight to 7 AM), advance to morning
    if current_time.hour >= 23 or current_time.hour < 7:
        current_time = current_time.replace(hour=8, minute=random.randint(5, 45), second=random.randint(0, 59))
        current_time += datetime.timedelta(days=1)
    
    # Format standard Google Form Timestamp (YYYY/MM/DD HH:MM:SS)
    timestamps.append(current_time)

timestamps.sort()

# Data containers
google_forms_records = []
clean_research_records = []

for i in range(NUM_RESPONSES):
    resp_id = f"RESP_{i+1:04d}"
    t_stamp = timestamps[i].strftime("%Y/%m/%d %I:%M:%S %p GMT+5:30")
    t_stamp_iso = timestamps[i].strftime("%Y-%m-%d %H:%M:%S")

    # Latent behavioral traits
    tech_reliance = np.clip(np.random.beta(4, 2), 0, 1)      # High digital penetration
    impulse_trait = np.clip(np.random.beta(3, 2.5), 0, 1)     # Likelihood of impulsive spending
    budget_discipline = np.clip(np.random.beta(2.5, 3), 0, 1) # Conscious budgeting
    allowance_tier = np.random.choice([0, 1, 2, 3, 4], p=[0.40, 0.35, 0.16, 0.06, 0.03])

    # Q1: Frequency of UPI
    freq_probs = [
        0.55 * tech_reliance + 0.25,        # Daily
        0.25 * tech_reliance + 0.10,        # Several times a week
        0.10 * (1 - tech_reliance) + 0.04,  # Once a week
        0.06 * (1 - tech_reliance) + 0.02,  # A few times a month
        0.04 * (1 - tech_reliance) + 0.01   # Rarely
    ]
    freq_probs = np.array(freq_probs) / sum(freq_probs)
    q1_val = np.random.choice(Q1_OPTIONS, p=freq_probs)
    is_daily = (q1_val == 'Daily')

    # Q3: Cash Carried (~68% carry < ₹500)
    if tech_reliance > 0.4:
        cash_probs = [0.70, 0.18, 0.08, 0.03, 0.01]
    else:
        cash_probs = [0.35, 0.30, 0.20, 0.10, 0.05]
    cash_probs = np.array(cash_probs) / sum(cash_probs)
    q3_val = np.random.choice(Q3_OPTIONS, p=cash_probs)

    # Q9: UPI Payments Feel Less Painful (~65% Yes)
    pain_prob_yes = 0.40 + 0.45 * tech_reliance - 0.15 * budget_discipline
    pain_prob_yes = np.clip(pain_prob_yes, 0.35, 0.88)
    pain_prob_no = (1 - pain_prob_yes) * 0.60
    pain_prob_notsure = 1 - (pain_prob_yes + pain_prob_no)
    q9_val = np.random.choice(Q9_OPTIONS, p=[pain_prob_yes, pain_prob_no, pain_prob_notsure])
    less_painful_flag = (q9_val == 'Yes')

    # Pre-UPI Spending (Q12) vs Post-UPI Spending (Q13 & Q2)
    pre_tier = allowance_tier
    if random.random() < 0.12:
        q12_val = 'Not applicable / Cannot remember'
    else:
        q12_val = Q12_OPTIONS[pre_tier]

    # Post-UPI jump
    post_tier = pre_tier
    jump_chance = 0.35 + 0.35 * impulse_trait + (0.15 if less_painful_flag else 0.0) - 0.20 * budget_discipline
    if random.random() < jump_chance and post_tier < 4:
        post_tier = min(4, post_tier + 1)
        if random.random() < 0.10 and post_tier < 4:
            post_tier = min(4, post_tier + 1)
    q13_val = Q13_OPTIONS[post_tier]

    # Q2: Monthly UPI Spending
    if random.random() < 0.85:
        q2_val = q13_val
    else:
        adj_tier = max(0, min(4, post_tier + np.random.choice([-1, 0, 1], p=[0.2, 0.6, 0.2])))
        q2_val = Q2_OPTIONS[adj_tier]

    # Q4: Spend More When Paying via UPI than Cash
    spend_more_score = 0.30 + 0.40 * impulse_trait + (0.25 if less_painful_flag else -0.10)
    p_yes = np.clip(spend_more_score, 0.15, 0.85)
    p_no = np.clip((1 - p_yes) * 0.6, 0.08, 0.5)
    p_maybe = max(0.01, 1 - p_yes - p_no)
    q4_val = np.random.choice(Q4_OPTIONS, p=[p_yes, p_no, p_maybe])

    # Likert scale generator
    def sample_likert(propensity, options):
        p = np.clip(propensity, 0.05, 0.95)
        w = [
            max(0.02, (1 - p)**2.5),
            max(0.04, (1 - p)**1.5 * p**0.5 * 2),
            max(0.06, 1.8 * p * (1 - p)),
            max(0.04, p**1.5 * (1 - p)**0.5 * 2),
            max(0.02, p**2.5)
        ]
        w = np.array(w) / sum(w)
        return np.random.choice(options, p=w)

    # Q5: Unplanned Purchases
    q5_val = sample_likert(0.15 + 0.70 * impulse_trait + (0.15 if is_daily else 0.0), Q5_OPTIONS)

    # Q6: Influence of Cashbacks/Discounts
    q6_val = sample_likert(0.20 + 0.60 * impulse_trait + 0.15 * tech_reliance, Q6_OPTIONS)

    # Q7: Checking Transaction History
    hist_prob = [
        0.20 + 0.50 * budget_discipline,
        0.30,
        0.30 * (1 - budget_discipline) + 0.10,
        0.15 * (1 - budget_discipline) + 0.05
    ]
    hist_prob = np.array(hist_prob) / sum(hist_prob)
    q7_val = np.random.choice(Q7_OPTIONS, p=hist_prob)

    # Q8: Regret Over UPI Purchases
    q8_val = sample_likert(0.10 + 0.65 * impulse_trait - 0.20 * budget_discipline + 0.10 * (1 if q4_val == 'Yes' else 0), Q8_OPTIONS)

    # Q10: Spending Has Increased
    has_increased = (post_tier > pre_tier) or (q4_val == 'Yes')
    if has_increased:
        p_inc_yes, p_inc_no, p_inc_ns = 0.78, 0.10, 0.12
    else:
        p_inc_yes, p_inc_no, p_inc_ns = 0.35, 0.45, 0.20
    q10_val = np.random.choice(Q10_OPTIONS, p=[p_inc_yes, p_inc_no, p_inc_ns])

    # Q11: Small-Value Convenience Purchases
    q11_val = sample_likert(0.30 + 0.50 * tech_reliance + 0.20 * impulse_trait, Q11_OPTIONS)

    # Q14: Rate Influence (1 to 10)
    raw_influence = (
        2.5
        + 1.0 * post_tier
        + 2.5 * impulse_trait
        + 2.0 * tech_reliance
        + (1.2 if less_painful_flag else -0.5)
        + np.random.normal(0, 0.9)
    )
    q14_val = int(np.clip(round(raw_influence), 1, 10))

    # Q15: Causes Overspending
    overspend_score = (
        0.15
        + (0.35 if is_daily else 0.05)
        + (0.30 if less_painful_flag else 0.0)
        + 0.25 * impulse_trait
        + 0.05 * (q14_val - 5)
        + (0.25 if q4_val == 'Yes' else -0.15)
        - 0.20 * budget_discipline
    )
    p_os_yes = np.clip(overspend_score, 0.05, 0.88)
    p_os_no = np.clip((1 - p_os_yes) * (0.50 + 0.30 * budget_discipline), 0.05, 0.70)
    p_os_maybe = max(0.02, 1 - p_os_yes - p_os_no)
    tot = p_os_yes + p_os_no + p_os_maybe
    q15_val = np.random.choice(Q15_OPTIONS, p=[p_os_yes/tot, p_os_no/tot, p_os_maybe/tot])

    # 1. Google Forms row (Exactly matching Google Forms export)
    google_forms_records.append({
        GF_COL_TIMESTAMP: t_stamp,
        GF_COL_Q1: q1_val,
        GF_COL_Q2: q2_val,
        GF_COL_Q3: q3_val,
        GF_COL_Q4: q4_val,
        GF_COL_Q5: q5_val,
        GF_COL_Q6: q6_val,
        GF_COL_Q7: q7_val,
        GF_COL_Q8: q8_val,
        GF_COL_Q9: q9_val,
        GF_COL_Q10: q10_val,
        GF_COL_Q11: q11_val,
        GF_COL_Q12: q12_val,
        GF_COL_Q13: q13_val,
        GF_COL_Q14: q14_val,
        GF_COL_Q15: q15_val
    })

    # 2. Research standard row (Clean feature headers)
    clean_research_records.append({
        'Respondent_ID': resp_id,
        'Timestamp': t_stamp_iso,
        'UPI_Frequency': q1_val,
        'Monthly_UPI_Spending': q2_val,
        'Cash_Carried': q3_val,
        'Spend_More_Than_Cash': q4_val,
        'Unplanned_Purchases_Frequency': q5_val,
        'Cashback_Discount_Influence': q6_val,
        'Checks_Transaction_History': q7_val,
        'Regret_UPI_Purchase': q8_val,
        'Payment_Less_Painful': q9_val,
        'Spending_Increased_With_UPI': q10_val,
        'Small_Value_Convenience_Purchases': q11_val,
        'Monthly_Spending_Before_UPI': q12_val,
        'Monthly_Spending_After_UPI': q13_val,
        'Influence_Rating_1_10': q14_val,
        'Causes_Overspending': q15_val
    })

df_gf = pd.DataFrame(google_forms_records)
df_clean = pd.DataFrame(clean_research_records)

# -------------------------------------------------------------
# Robust OpenXML Excel Generator with UTF-8 support
# -------------------------------------------------------------
def export_to_xlsx(dataframe, file_path, sheet_name="Form Responses 1"):
    headers = list(dataframe.columns)
    records = dataframe.values.tolist()
    
    shared_strings = []
    string_to_idx = {}
    
    def get_string_idx(s):
        s_str = str(s)
        if s_str not in string_to_idx:
            string_to_idx[s_str] = len(shared_strings)
            shared_strings.append(s_str)
        return string_to_idx[s_str]

    def col_to_letter(col_idx):
        result = ""
        while col_idx > 0:
            col_idx, remainder = divmod(col_idx - 1, 26)
            result = chr(65 + remainder) + result
        return result

    sheet_rows_xml = []
    
    # Header row
    hdr_cells = []
    for c_idx, h in enumerate(headers, start=1):
        cell_ref = f"{col_to_letter(c_idx)}1"
        s_id = get_string_idx(h)
        hdr_cells.append(f'<c r="{cell_ref}" t="s" s="1"><v>{s_id}</v></c>')
    sheet_rows_xml.append(f'<row r="1" ht="26" customHeight="1">{"".join(hdr_cells)}</row>')
    
    # Data rows
    for r_idx, row in enumerate(records, start=2):
        row_cells = []
        for c_idx, val in enumerate(row, start=1):
            cell_ref = f"{col_to_letter(c_idx)}{r_idx}"
            if isinstance(val, (int, np.integer)):
                row_cells.append(f'<c r="{cell_ref}"><v>{val}</v></c>')
            else:
                s_id = get_string_idx(val)
                row_cells.append(f'<c r="{cell_ref}" t="s"><v>{s_id}</v></c>')
        sheet_rows_xml.append(f'<row r="{r_idx}">{"".join(row_cells)}</row>')

    sheet_xml_content = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
    <sheetViews>
        <sheetView tabSelected="1" workbookViewId="0">
            <pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>
        </sheetView>
    </sheetViews>
    <sheetFormatPr defaultRowHeight="18"/>
    <sheetData>
        {"".join(sheet_rows_xml)}
    </sheetData>
</worksheet>'''

    si_elements = [f'<si><t>{saxutils.escape(s)}</t></si>' for s in shared_strings]
    sst_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="{len(shared_strings)}" uniqueCount="{len(shared_strings)}">
    {"".join(si_elements)}
</sst>'''

    styles_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
    <fonts count="2">
        <font><name val="Arial"/><sz val="10"/><color theme="1"/></font>
        <font><b/><name val="Arial"/><sz val="10"/><color rgb="FFFFFFFF"/></font>
    </fonts>
    <fills count="3">
        <fill><patternFill patternType="none"/></fill>
        <fill><patternFill patternType="gray125"/></fill>
        <fill><patternFill patternType="solid"><fgColor rgb="FF0F9D58"/></patternFill></fill>
    </fills>
    <borders count="1">
        <border><left/><right/><top/><bottom/></border>
    </borders>
    <cellStyleXfs count="1">
        <xf numFmtId="0" fontId="0" fillId="0" borderId="0"/>
    </cellStyleXfs>
    <cellXfs count="2">
        <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
        <xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1"/>
    </cellXfs>
</styleSheet>'''

    workbook_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
    <sheets>
        <sheet name="{saxutils.escape(sheet_name)}" sheetId="1" r:id="rId1"/>
    </sheets>
</workbook>'''

    workbook_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
    <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>
    <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''

    root_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>'''

    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Default Extension="xml" ContentType="application/xml"/>
    <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
    <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
    <Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>
    <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
</Types>'''

    with zipfile.ZipFile(file_path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', content_types)
        z.writestr('_rels/.rels', root_rels)
        z.writestr('xl/workbook.xml', workbook_xml)
        z.writestr('xl/_rels/workbook.xml.rels', workbook_rels)
        z.writestr('xl/worksheets/sheet1.xml', sheet_xml_content)
        z.writestr('xl/sharedStrings.xml', sst_xml)
        z.writestr('xl/styles.xml', styles_xml)


# -------------------------------------------------------------
# 1. EXPORT GOOGLE FORMS FORMAT (Exact Form Questions & Timestamps)
# CRITICAL: utf-8-sig adds the UTF-8 BOM so Excel opens ₹ and – without corruption
# -------------------------------------------------------------
gf_csv = "Google_Forms_UPI_Spending_Responses.csv"
gf_xlsx = "Google_Forms_UPI_Spending_Responses.xlsx"

df_gf.to_csv(gf_csv, index=False, encoding='utf-8-sig')
export_to_xlsx(df_gf, gf_xlsx, sheet_name="Form Responses 1")
print(f"[OK] Generated Google Forms Format CSV:   {gf_csv} (UTF-8 BOM, {len(df_gf)} rows)")
print(f"[OK] Generated Google Forms Format Excel: {gf_xlsx} (OpenXML, {len(df_gf)} rows)")

# -------------------------------------------------------------
# 2. EXPORT CLEAN RESEARCH DATASET (Short Headers for AIML)
# -------------------------------------------------------------
clean_csv = "UPI_Impact_Research_Data_Clean.csv"
clean_xlsx = "UPI_Impact_Research_Data_Clean.xlsx"

try:
    df_clean.to_csv(clean_csv, index=False, encoding='utf-8-sig')
    export_to_xlsx(df_clean, clean_xlsx, sheet_name="UPI_Survey_Data")
    print(f"[OK] Generated Research Dataset CSV:      {clean_csv} (UTF-8 BOM, {len(df_clean)} rows)")
    print(f"[OK] Generated Research Dataset Excel:    {clean_xlsx} (OpenXML, {len(df_clean)} rows)")
except Exception as e:
    print(f"Note on Clean dataset export: {e}")

# Also try writing original filename if unlocked
try:
    df_clean.to_csv("Impact_of_UPI_on_Spending_Behaviour_Dataset.csv", index=False, encoding='utf-8-sig')
    export_to_xlsx(df_clean, "Impact_of_UPI_on_Spending_Behaviour_Dataset.xlsx", sheet_name="UPI_Survey_Data")
    print("[OK] Updated original Impact_of_UPI_on_Spending_Behaviour_Dataset files")
except Exception:
    pass

print("\n--- Summary Verification ---")
print(f"Total Responses: {len(df_gf)}")
print(f"Columns Count:   {len(df_gf.columns)}")
print("Header Sample from Google Forms Export:")
for col in list(df_gf.columns)[:5]:
    print("  ->", col)
