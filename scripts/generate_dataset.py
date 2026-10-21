"""
UPI Spending Behaviour Dataset Generator
Generates 3,000 realistic, statistically coherent survey responses
matching the research questions, empirical distributions, and hypotheses
defined in PROJECT_CONTEXT.md.
Exports to both CSV and Excel (.xlsx) formats.
"""

import os
import sys
import random
import datetime
import csv
import zipfile
import xml.sax.saxutils as saxutils
import numpy as np
import pandas as pd

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

# Set reproducible random seed
np.random.seed(42)
random.seed(42)

NUM_RESPONSES = 3000

# Permitted categorical values
UPI_FREQUENCIES = ['Daily', 'Several times a week', 'Once a week', 'A few times a month', 'Rarely']
SPEND_BRACKETS = ['Below ₹5,000', '₹5,000–₹10,000', '₹10,001–₹20,000', '₹20,001–₹30,000', 'Above ₹30,000']
SPEND_BEFORE_OPTIONS = ['Below ₹5,000', '₹5,000–₹10,000', '₹10,001–₹20,000', '₹20,001–₹30,000', 'Above ₹30,000', 'Not applicable / Cannot remember']
CASH_CARRIED_OPTIONS = ['Less than ₹500', '₹500–₹1,000', '₹1,001–₹2,000', '₹2,001–₹5,000', 'More than ₹5,000']
LIKERT_OPTIONS = ['Never', 'Rarely', 'Sometimes', 'Often', 'Very often']
YES_NO_MAYBE = ['Yes', 'No', 'Maybe']
YES_NO_NOTSURE = ['Yes', 'No', 'Not sure']
CHECKS_HISTORY_OPTIONS = ['Yes, regularly', 'Sometimes', 'Rarely', 'Never']

# Midpoint maps for continuous alignment
SPEND_MIDPOINTS = {
    'Below ₹5,000': 3500.0,
    '₹5,000–₹10,000': 7500.0,
    '₹10,001–₹20,000': 15000.0,
    '₹20,001–₹30,000': 25000.0,
    'Above ₹30,000': 35000.0
}

data_rows = []

# Base start date for timestamps: 2024-01-15 to 2024-05-15
start_date = datetime.datetime(2024, 1, 15, 8, 30, 0)

for i in range(1, NUM_RESPONSES + 1):
    resp_id = f"RESP_{i:04d}"
    
    # Generate realistic survey submission timestamp
    random_seconds = random.randint(0, 120 * 24 * 3600)
    timestamp = start_date + datetime.timedelta(seconds=random_seconds)
    
    # Latent behavioral traits for respondent:
    # 1. Tech/Digital Reliance [0 to 1]
    # 2. Impulse Tendency [0 to 1]
    # 3. Budget / Financial Discipline [0 to 1]
    # 4. Income / Allowance tier [0, 1, 2, 3, 4]
    
    tech_reliance = np.clip(np.random.beta(4, 2), 0, 1)  # Skewed towards high digital reliance
    impulse_trait = np.clip(np.random.beta(3, 2.5), 0, 1)
    budget_discipline = np.clip(np.random.beta(2.5, 3), 0, 1)
    allowance_tier = np.random.choice([0, 1, 2, 3, 4], p=[0.40, 0.35, 0.16, 0.06, 0.03])
    
    # Q1: Frequency of UPI Usage (>75% Daily or Several times a week)
    freq_probs = [
        0.55 * tech_reliance + 0.25,        # Daily
        0.25 * tech_reliance + 0.10,        # Several times a week
        0.10 * (1 - tech_reliance) + 0.04,  # Once a week
        0.06 * (1 - tech_reliance) + 0.02,  # A few times a month
        0.04 * (1 - tech_reliance) + 0.01   # Rarely
    ]
    freq_probs = np.array(freq_probs) / sum(freq_probs)
    q1_freq = np.random.choice(UPI_FREQUENCIES, p=freq_probs)
    is_daily = (q1_freq == 'Daily')

    # Q3: Cash Carried (~68% carry < ₹500)
    if tech_reliance > 0.4:
        cash_probs = [0.70, 0.18, 0.08, 0.03, 0.01]
    else:
        cash_probs = [0.35, 0.30, 0.20, 0.10, 0.05]
    cash_probs = np.array(cash_probs) / sum(cash_probs)
    q3_cash = np.random.choice(CASH_CARRIED_OPTIONS, p=cash_probs)
    
    # Q9: UPI Payments Feel Less Painful / Noticeable than Cash (~65% Yes)
    pain_prob_yes = 0.40 + 0.45 * tech_reliance - 0.15 * budget_discipline
    pain_prob_yes = np.clip(pain_prob_yes, 0.35, 0.88)
    pain_prob_no = (1 - pain_prob_yes) * 0.60
    pain_prob_notsure = 1 - (pain_prob_yes + pain_prob_no)
    q9_pain = np.random.choice(YES_NO_NOTSURE, p=[pain_prob_yes, pain_prob_no, pain_prob_notsure])
    less_painful_flag = (q9_pain == 'Yes')
    
    # Pre-UPI Spending (Q12) vs Post-UPI Spending (Q13 & Q2)
    pre_tier = allowance_tier
    if random.random() < 0.12:
        q12_before = 'Not applicable / Cannot remember'
    else:
        q12_before = SPEND_BRACKETS[pre_tier]
    
    # Post-UPI spend bracket: on average 1 bracket jump due to friction reduction
    post_tier = pre_tier
    jump_chance = 0.35 + 0.35 * impulse_trait + (0.15 if less_painful_flag else 0.0) - 0.20 * budget_discipline
    if random.random() < jump_chance and post_tier < 4:
        post_tier = min(4, post_tier + 1)
        if random.random() < 0.10 and post_tier < 4:
            post_tier = min(4, post_tier + 1)
            
    q13_after = SPEND_BRACKETS[post_tier]
    
    # Q2: Monthly UPI Spending
    if random.random() < 0.85:
        q2_monthly_spend = q13_after
    else:
        adj_tier = max(0, min(4, post_tier + np.random.choice([-1, 0, 1], p=[0.2, 0.6, 0.2])))
        q2_monthly_spend = SPEND_BRACKETS[adj_tier]

    # Q4: Spend More When Paying via UPI than Cash
    spend_more_score = 0.30 + 0.40 * impulse_trait + (0.25 if less_painful_flag else -0.10)
    p_yes = np.clip(spend_more_score, 0.15, 0.85)
    p_no = np.clip((1 - p_yes) * 0.6, 0.08, 0.5)
    p_maybe = max(0.01, 1 - p_yes - p_no)
    q4_spend_more = np.random.choice(YES_NO_MAYBE, p=[p_yes, p_no, p_maybe])
    
    # Likert generators
    def sample_likert(propensity):
        p = np.clip(propensity, 0.05, 0.95)
        w = [
            max(0.02, (1 - p)**2.5),
            max(0.04, (1 - p)**1.5 * p**0.5 * 2),
            max(0.06, 1.8 * p * (1 - p)),
            max(0.04, p**1.5 * (1 - p)**0.5 * 2),
            max(0.02, p**2.5)
        ]
        w = np.array(w) / sum(w)
        return np.random.choice(LIKERT_OPTIONS, p=w)
    
    # Q5: Unplanned Purchases Frequency
    q5_unplanned = sample_likert(0.15 + 0.70 * impulse_trait + (0.15 if is_daily else 0.0))
    
    # Q6: Influence of Cashbacks/Discounts
    q6_cashback = sample_likert(0.20 + 0.60 * impulse_trait + 0.15 * tech_reliance)
    
    # Q7: Checking Transaction History Regularly
    hist_prob = [
        0.20 + 0.50 * budget_discipline,
        0.30,
        0.30 * (1 - budget_discipline) + 0.10,
        0.15 * (1 - budget_discipline) + 0.05
    ]
    hist_prob = np.array(hist_prob) / sum(hist_prob)
    q7_history = np.random.choice(CHECKS_HISTORY_OPTIONS, p=hist_prob)
    
    # Q8: Regret Over UPI Purchases
    q8_regret = sample_likert(0.10 + 0.65 * impulse_trait - 0.20 * budget_discipline + 0.10 * (1 if q4_spend_more == 'Yes' else 0))
    
    # Q10: Spending Has Increased Since Regular UPI Usage
    has_increased = (post_tier > pre_tier) or (q4_spend_more == 'Yes')
    if has_increased:
        p_inc_yes, p_inc_no, p_inc_ns = 0.78, 0.10, 0.12
    else:
        p_inc_yes, p_inc_no, p_inc_ns = 0.35, 0.45, 0.20
    q10_spend_inc = np.random.choice(YES_NO_NOTSURE, p=[p_inc_yes, p_inc_no, p_inc_ns])
    
    # Q11: Small-Value Convenience Purchases Frequency
    q11_convenience = sample_likert(0.30 + 0.50 * tech_reliance + 0.20 * impulse_trait)
    
    # Q14: Rate UPI Influence on Spending Behaviour (1 to 10)
    raw_influence = (
        2.5
        + 1.0 * post_tier
        + 2.5 * impulse_trait
        + 2.0 * tech_reliance
        + (1.2 if less_painful_flag else -0.5)
        + np.random.normal(0, 0.9)
    )
    q14_influence = int(np.clip(round(raw_influence), 1, 10))
    
    # Q15: Belief that UPI Causes Overspending (Target Feature)
    overspend_score = (
        0.15
        + (0.35 if is_daily else 0.05)
        + (0.30 if less_painful_flag else 0.0)
        + 0.25 * impulse_trait
        + 0.05 * (q14_influence - 5)
        + (0.25 if q4_spend_more == 'Yes' else -0.15)
        - 0.20 * budget_discipline
    )
    p_os_yes = np.clip(overspend_score, 0.05, 0.88)
    p_os_no = np.clip((1 - p_os_yes) * (0.50 + 0.30 * budget_discipline), 0.05, 0.70)
    p_os_maybe = max(0.02, 1 - p_os_yes - p_os_no)
    total_p = p_os_yes + p_os_no + p_os_maybe
    q15_overspend = np.random.choice(YES_NO_MAYBE, p=[p_os_yes/total_p, p_os_no/total_p, p_os_maybe/total_p])
    
    data_rows.append({
        'Respondent_ID': resp_id,
        'Timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'UPI_Frequency': q1_freq,
        'Monthly_UPI_Spending': q2_monthly_spend,
        'Cash_Carried': q3_cash,
        'Spend_More_Than_Cash': q4_spend_more,
        'Unplanned_Purchases_Frequency': q5_unplanned,
        'Cashback_Discount_Influence': q6_cashback,
        'Checks_Transaction_History': q7_history,
        'Regret_UPI_Purchase': q8_regret,
        'Payment_Less_Painful': q9_pain,
        'Spending_Increased_With_UPI': q10_spend_inc,
        'Small_Value_Convenience_Purchases': q11_convenience,
        'Monthly_Spending_Before_UPI': q12_before,
        'Monthly_Spending_After_UPI': q13_after,
        'Influence_Rating_1_10': q14_influence,
        'Causes_Overspending': q15_overspend
    })

df = pd.DataFrame(data_rows)

# Output filenames
csv_path = 'Impact_of_UPI_on_Spending_Behaviour_Dataset.csv'
xlsx_path = 'Impact_of_UPI_on_Spending_Behaviour_Dataset.xlsx'

# Save CSV
df.to_csv(csv_path, index=False, encoding='utf-8')
print(f" Saved CSV:  {csv_path} ({len(df)} rows)")

# Save Excel XLSX using OpenXML
def create_xlsx(dataframe, file_path, sheet_name="UPI_Survey_Data"):
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
    sheet_rows_xml.append(f'<row r="1" ht="24" customHeight="1">{"".join(hdr_cells)}</row>')
    
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
    <sheetFormatPr defaultRowHeight="16"/>
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
        <font><name val="Calibri"/><sz val="11"/><color theme="1"/></font>
        <font><b/><name val="Calibri"/><sz val="11"/><color rgb="FFFFFFFF"/></font>
    </fonts>
    <fills count="3">
        <fill><patternFill patternType="none"/></fill>
        <fill><patternFill patternType="gray125"/></fill>
        <fill><patternFill patternType="solid"><fgColor rgb="FF1E3A8A"/></patternFill></fill>
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

create_xlsx(df, xlsx_path)
print(f" Saved Excel: {xlsx_path} ({len(df)} rows)")

print("\n--- Empirical Summary Verification ---")
print(f"Daily UPI Users: {(df['UPI_Frequency'] == 'Daily').mean()*100:.1f}%")
print(f"Frequent Users (Daily + Several times a week): {df['UPI_Frequency'].isin(['Daily', 'Several times a week']).mean()*100:.1f}%")
print(f"Carry < Rs.500: {(df['Cash_Carried'] == 'Less than ₹500').mean()*100:.1f}%")
print(f"Find UPI Less Painful: {(df['Payment_Less_Painful'] == 'Yes').mean()*100:.1f}%")
print(f"Overspending Rate (Causes_Overspending == 'Yes'): {(df['Causes_Overspending'] == 'Yes').mean()*100:.1f}%")
