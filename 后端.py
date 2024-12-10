from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os
import pandas as pd
from io import BytesIO

app = FastAPI()

# 提取 PDF 数据的函数（使用你的现有代码）
def extract_data_from_pdf(pdf_path, filename):
    # 你的 PDF 提取逻辑
    pass

@app.post("/process-pdf/")
async def process_pdf(file: UploadFile = File(...)):
    temp_dir = "/tmp"
    temp_file = os.path.join(temp_dir, file.filename)

    # 保存上传的文件
    with open(temp_file, "wb") as f:
        f.write(await file.read())

    # 调用数据提取函数
    data = extract_data_from_pdf(temp_file, file.filename)

    # 创建 DataFrame 并保存为 Excel
    df = pd.DataFrame(data)
    output_file = os.path.join(temp_dir, "extracted_data.xlsx")
    df.to_excel(output_file, index=False)

    # 删除临时文件
    os.remove(temp_file)

    return FileResponse(output_file, filename="extracted_data.xlsx")
  #部署到支持的云平台后，记下 API 地址（例如 https://your-api-host.com/process-pdf/）
