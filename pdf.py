from aip import AipOcr # 百度api
import json
import os
from PyPDF2 import PdfReader

'''配置APPID、API_KEY和SECRET_KEY'''
with open('config/baidu_ocr.json') as config_file:
    config = json.load(config_file)

# 从配置中提取需要的凭证信息
credentials = config["Credentials"]
'''初始化client'''
client = AipOcr(credentials["APP_ID"], credentials["API_KEY"], credentials["SECRET_KEY"])

'''读取文件'''
def get_file_content(file_path):
    # rb: binary and read-only
    with open(file_path, 'rb') as fp:
        return fp.read()
    
# pdf_file = get_file_content('upload/pdf/test.pdf')

# for i in range(1, 4):
#     options = {}
#     options["pdf_file_num"] = f"{i}"
#     res_pdf = client.basicGeneralPdf(pdf_file, options)
#     print(res_pdf)

reader = PdfReader('upload/pdf/test.pdf')
total_pages = len(reader.pages)
for i in range(0, total_pages):
    page = reader.pages[i]
    print(page.extract_text())
