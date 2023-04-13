import re
import PyPDF2
import pdfplumber
# from operations import itemgetter

def find_chapters(page_text):
    patterns = [
        r"\b(?:第)?\s*(\d+)\s*(?:章)?",
        r"\((\d+)\)",
        r"\b(?:Chapter)?\s*(\d+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, page_text, re.I)
        if match:
            return int(match.group(1))

    return None
def curves_to_edges(cs):
    """See https://github.com/jsvine/pdfplumber/issues/127"""
    edges = []
    for c in cs:
        edges += pdfplumber.utils.rect_to_edges(c)
    return edges
bboxes = []

def not_within_bboxes(obj):
    """Check if the object is in any of the table's bbox."""
    def obj_in_bbox(_bbox):
        """See https://github.com/jsvine/pdfplumber/blob/stable/pdfplumber/table.py#L404"""
        v_mid = (obj["top"] + obj["bottom"]) / 2
        h_mid = (obj["x0"] + obj["x1"]) / 2
        x0, top, x1, bottom = _bbox
        return (h_mid >= x0) and (h_mid < x1) and (v_mid >= top) and (v_mid < bottom)
    return not any(obj_in_bbox(__bbox) for __bbox in bboxes)

def split_pdf(input_pdf, output_pdf_prefix):
    with pdfplumber.open(input_pdf) as pdf:
        total_pages = len(pdf.pages)

        page_indices = []
        sections = []
        tables = []
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            ts = {
                "vertical_strategy": "explicit",
                "horizontal_strategy": "explicit",
                "explicit_vertical_lines": curves_to_edges(page.curves + page.edges),
                "explicit_horizontal_lines": curves_to_edges(page.curves + page.edges),
                "intersection_y_tolerance": 10,
            }
            global bboxes
            bboxes = [table.bbox for table in page.find_tables(table_settings=ts)]
            page_text=page.filter(not_within_bboxes).extract_text()
            table_settings = {
                "vertical_strategy": "text",
                "horizontal_strategy": "text"
            }
            table = page.extract_tables(table_settings)
            if len(table) > 0:
                tables.append(table)
            # print(tables)
            rx = re.compile(r'''
                ^
                (?:Section\ )?(\d+\.+\d+)+
                [\s\S]*?
                (?=^(?:Section\ )?(\d+\.+\d+)+|\Z)

                ''', re.VERBOSE | re.MULTILINE)

            parts = [match.group(0) for match in rx.finditer(page_text)]
            # print(parts)
            for part in parts:
                if len(part) > 0:
                    sections.append(part)
            # if len(parts) > 0:
            #     sections.append(parts)
            # if find_chapters(page_text):
            #     page_indices.append(i)
        print(f"Total {len(sections)} parts.")
        print(f"Total {len(tables)} tables")
        # page_indices.append(total_pages)

        for i, start_page in enumerate(page_indices[:-1]):
            end_page = page_indices[i + 1]
            # with open(f"{output_pdf_prefix}_chapter{i + 1}.pdf", "wb") as output:
            #     with open(input_pdf, "rb") as input:
            #         pdf_reader = PyPDF2.PdfFileReader(input)
            #         writer = PyPDF2.PdfFileWriter()
            #         for j in range(start_page, end_page):
            #             writer.add_page(pdf_reader.getPage(j)
            #         writer.write(output)

input_pdf = "D:\\Code\\CognitiveSearchGPT\\backend\\data\\2022_CMB_Report.pdf"  # 请将该路径替换为实际的输入PDF路径
output_pdf_prefix = "D:\\Code\\CognitiveSearchGPT\\backend\\data\\CMB\\CMB_Report"    # 输出文件的前缀
split_pdf(input_pdf, output_pdf_prefix)