import re
import PyPDF2
import pdfplumber
<<<<<<< HEAD

def find_chapters(page_text):
    patterns = [
        # r"\b(?:第)?\s*(\d+)\s*(?:节)?",
        # r"\((\d+)\)",
        r"^([1-9]\.*)+\s[\u4E00-\u9FA5A-Za-z0-9_]+"
    ]

    for pattern in patterns:
        # rx = re.compile(r'''^(([1-9]\.*)+\s[\u4E00-\u9FA5A-Za-z0-9_]+)''', re.M|re.DOTALL)
        # rx_blanks=re.compile(r"\W+")
        # match = re.search(pattern, page_text, flags=re.M)

        # for match in rx.finditer(page_text):
        #     title, sequence = match.groups()
        #     title = title.strip()
        #     sequence = rx_blanks.sub("",sequence)
        #     print(f"Title: {title}")
        #     print(f"Sequence: {sequence}")
        rx = re.compile(r'''
                ^
                (?:Section\ )?\d+\.+\d+
                [\s\S]*?
                (?=^(?:Section\ )?\d+\.+\d+|\Z)

                ''', re.VERBOSE | re.MULTILINE)

        parts = [match.group(0) for match in rx.finditer(page_text)]
        print(parts)
        return parts
        # if match:
        #     # print(match.group)
        #     return int(match.group(1))

    return None
def splitkeep(s, regex):
    split = re.split(regex, s)
    return [substr for substr in split[:-1]] + [split[-1]]
=======
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
>>>>>>> a2d05e99a2db2e212c68a162cf50c253aca45c51

def split_pdf(input_pdf, output_pdf_prefix):
    with pdfplumber.open(input_pdf) as pdf:
        total_pages = len(pdf.pages)
<<<<<<< HEAD
        paragraphs = []
        page_indices = []
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            splited_text = find_chapters(page_text)
            if len(splited_text) > 0:
                for text in splited_text:
                    paragraphs.append(text)
            # if find_chapters(page_text):
                # print(f"page {i}: {page_text}")
                # page_indices.append(i)
        # print(f"total: {len(page_indices)} pages.")
        # page_indices.append(total_pages)
        print(f"Total split into {len(paragraphs)} sections.")
        for i, start_page in enumerate(page_indices[:-1]):
            end_page = page_indices[i + 1]
            with open(f"{output_pdf_prefix}_chapter{i + 1}.pdf", "wb") as output:
                with open(input_pdf, 'rb') as book:
                    book_reader = PyPDF2.PdfReader(book)
                    writer = PyPDF2.PdfWriter()
                    # for j in range(start_page, end_page):
                        # writer.add_page(pdf.pages[j].page_obj)
                        # writer.add_page(book_reader.pages[j])

                # writer.write(output)

input_pdf = "D:\\Code\\CognitiveSearchChatGPTDemo\\backend\\data\\2022_CMB_Report.pdf"  # 请将该路径替换为实际的输入PDF路径
output_pdf_prefix = "D:\\Code\\CognitiveSearchChatGPTDemo\\backend\\data\\\\CMB\\2022_CMB_Report"    # 输出文件的前缀
=======

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
>>>>>>> a2d05e99a2db2e212c68a162cf50c253aca45c51
split_pdf(input_pdf, output_pdf_prefix)