# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2025-3-27
# Description   : pdf去掉水印
# pip install pymupdf
# *********************************************************************

import fitz  # PyMuPDF
from itertools import product


def remove_watermark_from_pdf(input_pdf_path, output_pdf_path):
    # 打开PDF文件
    pdf_document = fitz.open(input_pdf_path)

    # 创建一个新的PDF文档用于保存去除水印后的内容
    new_pdf_document = fitz.open()

    # 遍历每一页
    for page_num in range(len(pdf_document)):
        # 加载页面
        page = pdf_document.load_page(page_num)

        # 获取页面的位图表示
        pixmap = page.get_pixmap()

        # 遍历每个像素点，检查其是否代表水印
        # 这里假设水印的RGB值之和大于某个阈值（例如600）
        for pos in product(range(pixmap.width), range(pixmap.height)):
            rgb = pixmap.pixel(pos[0], pos[1])
            if sum(rgb) >= 600:
                pixmap.set_pixel(pos[0], pos[1], (255, 255, 255))  # 将水印像素点设置为白色

        # 创建新页面
        new_page = new_pdf_document.new_page(width=page.rect.width, height=page.rect.height)

        # 将处理后的位图转换为图像数据
        img_data = pixmap.tobytes("png")

        # 在新页面上插入图像
        new_page.insert_image(
            page.rect,  # 图像占据整个页面
            stream=img_data
        )

    # 保存新的PDF文档
    new_pdf_document.save(output_pdf_path)

    # 关闭PDF文档
    pdf_document.close()
    new_pdf_document.close()


# 调用函数去除水印
input_pdf_path = "/Users/linghuchong/Desktop/1/test.pdf"  # 输入PDF文件路径
output_pdf_path = "/Users/linghuchong/Desktop/1/test55.pdf"  # 输出PDF文件路径
remove_watermark_from_pdf(input_pdf_path, output_pdf_path)
