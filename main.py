from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from PIL import Image, ImageFilter, ImageOps
import fitz  # PyMuPDF
import io
import os

app = FastAPI()

@app.post("/enhance_pdf")
async def enhance_pdf(file: UploadFile):
    # 读取 PDF
    input_bytes = await file.read()
    pdf = fitz.open(stream=input_bytes, filetype="pdf")

    enhanced_pdf = fitz.open()  # 输出 PDF

    for page_num in range(len(pdf)):
        page = pdf[page_num]

        # 将 PDF 页面渲染为高分辨率图像
        zoom = 2.0  # 放大 2 倍
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False)

        img = Image.open(io.BytesIO(pix.tobytes("png")))

        # 图像增强流程
        img = img.filter(ImageFilter.MedianFilter(size=3))  # 去噪
        img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))  # 锐化
        img = ImageOps.autocontrast(img, cutoff=2)  # 自动对比度

        # 转回 PDF 页面
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")
        rect = fitz.Rect(0, 0, img.width, img.height)
        new_page = enhanced_pdf.new_page(width=rect.width, height=rect.height)
        new_page.insert_image(rect, stream=img_bytes.getvalue())

    # 输出增强后的 PDF
    output_path = "enhanced.pdf"
    enhanced_pdf.save(output_path)
    enhanced_pdf.close()

    return FileResponse(output_path, media_type="application/pdf", filename="enhanced.pdf")
