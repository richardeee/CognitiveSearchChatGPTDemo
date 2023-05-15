import os
import sys
import win32com.client as client
from openpyxl import load_workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
import shutil
import time

def convert_office_to_pdf(input_file, output_file):
    try:
        word_app = client.CreateObject('Word.Application')
        word_app.Visible=False
        time.sleep(3)
        doc = word_app.Documents.Open(input_file)
        doc.SaveAs(output_file, FileFormat=17)  #17 corresponds to PDF format
        doc.Close()
        word_app.Quit()
        print(f"Converted '{input_file}' to '{output_file}'")
    except:
        print(f"could not convert {input_file}")

def convert_ppt_to_pdf(input_file, output_file):
    print(f"converting: {input_file}")
    try:
        powerpoint = client.CreateObject('Powerpoint.Application')
        powerpoint.Visible=False
        time.sleep(3)
        deck = powerpoint.Presentations.Open(input_file)
        deck.SaveAs(output_file, FileFormat=32)
        deck.Close()
        powerpoint.Quit()
        print(f"Converted '{input_file}' to '{output_file}'")
    except:
        print(f"could not convert {input_file}")


def convert_xlsx_to_pdf(input_file, output_file):
    try:
        wb = load_workbook(input_file)
        file_name = os.path.splitext(input_file)[0]

        for ws in wb.worksheets:
            c = canvas.Canvas(output_file, pagesize=letter)

            for row in ws.values:
                row_str = ','.join(map(str, row))
                c.drawString(10, 800, row_str)
                c.showPage()

            c.save()
        print(f"Converted '{input_file}' to '{output_file}'")
    except:
        print(f"could not convert {input_file}")

def convert_jpg_to_pdf(input_file, output_file):
    try:
        image = Image.open(input_file)
        pdf_image = image.convert('RGB')
        pdf_image.save(output_file)
        print(f"Converted '{input_file}' to '{output_file}'")
    except:
        print(f"could not convert {input_file}")
def copy_file(input_file, output_file):
    shutil.copy(input_file, output_file)

def copy_pdf(input_file, output_file):
    #copy file from input_file to output_file
    shutil.copy(input_file, output_file)

formats_to_convert = ['.docx', '.xlsx', '.ppt', '.doc', '.jpg']
converters = {
    '.docx': convert_office_to_pdf,
    '.doc': convert_office_to_pdf,
    '.ppt': convert_ppt_to_pdf,
    '.pptx': convert_ppt_to_pdf,
    '.xlsx': convert_xlsx_to_pdf,
    '.jpg': convert_jpg_to_pdf,
<<<<<<< HEAD
    '.pdf': copy_file,
}

data_folder = 'D:/Code/CognitiveSearchChatGPTDemo/backend/data/O365/'
=======
    '.pdf': copy_pdf,
}

data_folder = 'D:/Code/CognitiveSearchGPT/backend/data/Portal/'
>>>>>>> 189e70827624452d017320b48bce853be1568c8f

for subdir, dirs, files in os.walk(data_folder):
    for file in files:
        file_extension = os.path.splitext(file)[1]
        if file_extension.lower() in formats_to_convert:
            input_file = os.path.join(subdir, file)
            
            pdf_dir = os.path.join(subdir, 'pdf')
            os.makedirs(pdf_dir, exist_ok=True)  # 创建pdf文件夹如果不存在
            
            output_file = os.path.join(pdf_dir, file.replace(file_extension, '.pdf'))
            converters[file_extension.lower()](input_file, output_file)
            