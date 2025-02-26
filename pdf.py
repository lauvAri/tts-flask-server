from aip import AipOcr # 百度api
import json
import os
from PyPDF2 import PdfReader
#from pdfminer.high_level import extract_text
import fitz #PyMuPDF
from PIL import Image
import io
import base64

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


def get_pdf_page(pdf_path, page_num = 1):
    try:
        # 打开PDF文件
        doc = fitz.open(pdf_path)
        total_pages = doc.page_count # 总页数
        # 检查页码是否有效
        if (page_num < 1 or page_num > total_pages):
            msg = "页码超出范围"
            return False, msg
        # 获取指定页面
        page = doc.load_page(page_num - 1)
        pix = page.get_pixmap()  # 转为图像
        # 图像数据保存到内存中
        img_bytes = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_bytes))
        # 图像保存到内存缓冲区域
        img_buffer = io.BytesIO()
        img.save(img_buffer, format = "PNG")
        img_buffer.seek(0)

        img_base64 = base64.b64encode(img_buffer.getvalue()).decode("utf-8")
        # 返回图像数据和总页数
        response = {
            "total_pages": total_pages,
            "current_page": page_num,
            "image_data": f"data:image/png;base64,{img_base64}"
        }
        return True, response
        
    except Exception as e:
        msg = str(e)
        return False, msg

if __name__ == "__main__":
    flag, msg = get_pdf_page("upload/pdf/test.pdf", page_num=2)
    print(flag, msg)