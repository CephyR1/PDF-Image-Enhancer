# PDF-Image-Enhancer
# PDF Image Enhancer Plugin for Dify

## 功能
- 接收一个 PDF 文件
- 每页渲染为高分辨率图像
- 图像增强处理：
  - 去噪 (MedianFilter)
  - 锐化 (UnsharpMask)
  - 对比度增强 (autocontrast)
- 输出增强后的 PDF，适合送入 OCR 引擎

## API
- `POST /enhance_pdf`
- 输入：PDF 文件
- 输出：增强后的 PDF 文件

## 部署
```bash
docker build -t pdf-image-enhancer .
docker run -p 8000:8000 pdf-image-enhancer
