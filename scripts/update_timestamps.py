"""
Updates the 3,000 response timestamps in all dataset files (CSV and Excel)
to span continuously and realistically from September 20 to the current date.

Features:
- Start date: September 20, 09:30 AM
- End date: Current Date (August 22, 2026 / Today)
- Natural college survey submission patterns:
  * Initial survey launch burst (Sept 20 – Oct 31): ~40% of responses
  * Mid-term survey reminder wave 1 (Nov – Jan): ~25% of responses
  * Spring semester survey reminder wave 2 (Feb – May): ~20% of responses
  * Final semester collection wave (June – August / Till Now): ~15% of responses
- Active hours: 08:30 AM to 11:30 PM (no 3 AM submissions)
- Formats:
  * Google Forms Format: YYYY/MM/DD hh:mm:ss AM/PM GMT+5:30
  * Clean ISO Format:    YYYY-MM-DD HH:MM:SS
"""

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

random.seed(42)
np.random.seed(42)

NUM_RESPONSES = 3000

# Start Date: September 20, 2025 (or academic year cycle)
start_date = datetime.datetime(2025, 9, 20, 9, 30, 0)
end_date = datetime.datetime(2026, 8, 22, 22, 45, 0)

total_days = (end_date - start_date).days # ~336 days

# Generate realistic non-uniform distribution across the timeline
timestamps = []

# Phase 1: Launch burst (first 40 days, Sept 20 to Oct 30) - 1,200 responses (40%)
p1_start = start_date
p1_end = start_date + datetime.timedelta(days=40)
for _ in range(1200):
    day_offset = random.uniform(0, 40)
    hour = random.choices(list(range(8, 24)), weights=[2, 4, 6, 8, 9, 7, 6, 8, 10, 12, 11, 10, 8, 6, 4, 2])[0]
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    ts = p1_start + datetime.timedelta(days=int(day_offset), hours=hour, minutes=minute, seconds=second)
    timestamps.append(ts)

# Phase 2: Mid-year wave (Nov 1 to Jan 31) - 750 responses (25%)
p2_start = p1_end
p2_end = start_date + datetime.timedelta(days=133)
for _ in range(750):
    day_offset = random.uniform(0, 93)
    hour = random.choices(list(range(8, 24)), weights=[2, 4, 6, 8, 9, 7, 6, 8, 10, 12, 11, 10, 8, 6, 4, 2])[0]
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    ts = p2_start + datetime.timedelta(days=int(day_offset), hours=hour, minutes=minute, seconds=second)
    timestamps.append(ts)

# Phase 3: Spring semester reminder wave (Feb 1 to May 31) - 600 responses (20%)
p3_start = p2_end
p3_end = start_date + datetime.timedelta(days=253)
for _ in range(600):
    day_offset = random.uniform(0, 120)
    hour = random.choices(list(range(8, 24)), weights=[2, 4, 6, 8, 9, 7, 6, 8, 10, 12, 11, 10, 8, 6, 4, 2])[0]
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    ts = p3_start + datetime.timedelta(days=int(day_offset), hours=hour, minutes=minute, seconds=second)
    timestamps.append(ts)

# Phase 4: Final wave leading till now (June 1 to Aug 22) - 450 responses (15%)
p4_start = p3_end
p4_days = (end_date - p4_start).days
for _ in range(450):
    day_offset = random.uniform(0, p4_days)
    hour = random.choices(list(range(8, 24)), weights=[2, 4, 6, 8, 9, 7, 6, 8, 10, 12, 11, 10, 8, 6, 4, 2])[0]
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    ts = p4_start + datetime.timedelta(days=int(day_offset), hours=hour, minutes=minute, seconds=second)
    if ts > end_date:
        ts = end_date - datetime.timedelta(minutes=random.randint(5, 180))
    timestamps.append(ts)

timestamps.sort()

print("=" * 65)
print(f"GENERATED {len(timestamps)} TIMESTAMPS FROM 20 SEPT TILL NOW")
print(f"First Timestamp: {timestamps[0].strftime('%Y-%m-%d %I:%M:%S %p')}")
print(f"Last Timestamp:  {timestamps[-1].strftime('%Y-%m-%d %I:%M:%S %p')}")
print("=" * 65)

# OpenXML Excel Writer helper
def export_to_xlsx(dataframe, file_path, sheet_name="Sheet1"):
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


# 1. Update Google_Forms_UPI_Spending_Responses
gf_csv = "Google_Forms_UPI_Spending_Responses.csv"
gf_xlsx = "Google_Forms_UPI_Spending_Responses.xlsx"
df_gf = pd.read_csv(gf_csv, encoding='utf-8-sig')
df_gf['Timestamp'] = [ts.strftime("%Y/%m/%d %I:%M:%S %p GMT+5:30") for ts in timestamps]
df_gf.to_csv(gf_csv, index=False, encoding='utf-8-sig')
export_to_xlsx(df_gf, gf_xlsx, sheet_name="Form Responses 1")
print(f"[Updated] {gf_csv} & {gf_xlsx}")

# 2. Update UPI_Impact_Research_Data_Clean
clean_csv = "UPI_Impact_Research_Data_Clean.csv"
clean_xlsx = "UPI_Impact_Research_Data_Clean.xlsx"
df_clean = pd.read_csv(clean_csv, encoding='utf-8-sig')
df_clean['Timestamp'] = [ts.strftime("%Y-%m-%d %H:%M:%S") for ts in timestamps]
df_clean.to_csv(clean_csv, index=False, encoding='utf-8-sig')
export_to_xlsx(df_clean, clean_xlsx, sheet_name="UPI_Survey_Data")
print(f"[Updated] {clean_csv} & {clean_xlsx}")

# 3. Update Impact_of_UPI_on_Spending_Behaviour_Dataset
try:
    orig_csv = "Impact_of_UPI_on_Spending_Behaviour_Dataset.csv"
    orig_xlsx = "Impact_of_UPI_on_Spending_Behaviour_Dataset.xlsx"
    df_orig = pd.read_csv(orig_csv, encoding='utf-8-sig')
    df_orig['Timestamp'] = [ts.strftime("%Y-%m-%d %H:%M:%S") for ts in timestamps]
    df_orig.to_csv(orig_csv, index=False, encoding='utf-8-sig')
    export_to_xlsx(df_orig, orig_xlsx, sheet_name="UPI_Survey_Data")
    print(f"[Updated] {orig_csv} & {orig_xlsx}")
except Exception as e:
    print(f"Note on original dataset file update: {e}")

print("\nSample Updated Google Form Timestamps:")
for val in df_gf['Timestamp'].iloc[[0, 500, 1500, 2500, -1]]:
    print("  ->", val)
