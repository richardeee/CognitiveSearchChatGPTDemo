import re
import PyPDF2
import pdfplumber

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

def split_pdf(input_pdf, output_pdf_prefix):
    with pdfplumber.open(input_pdf) as pdf:
        total_pages = len(pdf.pages)
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
split_pdf(input_pdf, output_pdf_prefix)