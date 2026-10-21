"""
Native CSV to XLSX converter using Python built-in standard library (zipfile, xml.sax.saxutils).
Zero third-party dependencies required. Creates standard ECMA-376 OpenXML Spreadsheet.
"""

import csv
import zipfile
import io
import xml.sax.saxutils as saxutils

def convert_csv_to_xlsx(csv_path, xlsx_path, sheet_name="UPI_Survey_Data"):
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = list(csv.reader(f))
        
    if not reader:
        print("CSV is empty.")
        return

    # Build Shared Strings Table
    shared_strings = []
    string_to_idx = {}
    
    def get_string_idx(s):
        if s not in string_to_idx:
            string_to_idx[s] = len(shared_strings)
            shared_strings.append(s)
        return string_to_idx[s]

    def col_to_letter(col_idx):
        result = ""
        while col_idx > 0:
            col_idx, remainder = divmod(col_idx - 1, 26)
            result = chr(65 + remainder) + result
        return result

    # Prepare sheet rows XML
    sheet_rows_xml = []
    
    for row_idx, row in enumerate(reader, start=1):
        row_cells_xml = []
        for col_idx, val in enumerate(row, start=1):
            cell_ref = f"{col_to_letter(col_idx)}{row_idx}"
            # Check if numeric (integer only for clean formatting or string)
            if row_idx > 1 and val.isdigit():
                # numeric cell
                row_cells_xml.append(f'<c r="{cell_ref}"><v>{val}</v></c>')
            else:
                str_idx = get_string_idx(val)
                # Header row style s="1", data row string style s="0" or s="2"
                style_attr = ' s="1"' if row_idx == 1 else ''
                row_cells_xml.append(f'<c r="{cell_ref}" t="s"{style_attr}><v>{str_idx}</v></c>')
        sheet_rows_xml.append(f'<row r="{row_idx}">{"".join(row_cells_xml)}</row>')

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

    # Build sharedStrings.xml
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

    with zipfile.ZipFile(xlsx_path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', content_types)
        z.writestr('_rels/.rels', root_rels)
        z.writestr('xl/workbook.xml', workbook_xml)
        z.writestr('xl/_rels/workbook.xml.rels', workbook_rels)
        z.writestr('xl/worksheets/sheet1.xml', sheet_xml_content)
        z.writestr('xl/sharedStrings.xml', sst_xml)
        z.writestr('xl/styles.xml', styles_xml)

    print(f"Successfully generated native Excel XLSX: {xlsx_path}")

if __name__ == '__main__':
    convert_csv_to_xlsx(
        'Impact_of_UPI_on_Spending_Behaviour_Dataset.csv',
        'Impact_of_UPI_on_Spending_Behaviour_Dataset.xlsx'
    )
