import os
import re
import fitz  # PyMuPDF
import pdfplumber
import pandas as pd

# PDF文件路径
pdf_folder_path = "F:\pythonProject\通知单"

# 提取数据的函数
def extract_data_from_pdf(pdf_path, filename):
    # 打开PDF文件
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()

    # 初始化存储数据的字典
    data = {
        "文件名": filename,  # 添加文件名字段
        "用户编号": None,
        "市场化属性分类": None,
        "应缴电费合计金额": None,
        "用电地址": None,
        "表计资产编号": [],
        "示数类型": [],
        "上次表示数": [],
        "本次表示数": [],
        "倍率": [],
        "抄见电量（千瓦时)": [],
        "换表电量（千瓦时)": [],
        "变/线损电量（千瓦时)": [],
        "合计电量（千瓦时)": [],
    }

    # 提取用户编号
    if "用户编号：" in text:
        data["用户编号"] = re.search(r'用户编号：(\d+)', text).group(1)

    # 提取市场化属性分类
    if "市场化属性分类：" in text:
        data["市场化属性分类"] = re.search(r'市场化属性分类：([\s\S]+?)\s+', text).group(1).strip()

    # 提取应缴电费合计金额
    if "应缴电费合计金额" in text:
        data["应缴电费合计金额"] = re.search(r'应缴电费合计金额￥([\d\.]+)元', text).group(1)

    # 提取用电地址
    if "用电地址：" in text:
        data["用电地址"] = re.search(r'用电地址：([\s\S]+?)用电开始时间', text).group(1).strip().replace('\n', '')

    # 使用pdfplumber提取电量信息
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:  # 遍历每一页
            tables = page.extract_tables()
            for table in tables:
                if '表计资产编号' in table[0][0]:
                    for row in table[1:]:  # 跳过表头
                        if any(meter_type in row[1] for meter_type in ["有功总", "尖峰", "峰", "平", "谷"]):
                            data["表计资产编号"].append(row[0])
                            data["示数类型"].append(row[1])
                            data["上次表示数"].append(row[2])
                            data["本次表示数"].append(row[3])
                            data["倍率"].append(row[4])
                            data["抄见电量（千瓦时)"].append(row[5])
                            data["换表电量（千瓦时)"].append(row[6])
                            data["变/线损电量（千瓦时)"].append(row[8])
                            data["合计电量（千瓦时)"].append(row[12])

    document.close()
    return data

# 初始化DataFrame
df = pd.DataFrame(columns=[
    "文件名", "用户编号", "市场化属性分类", "应缴电费合计金额", "用电地址",
    "表计资产编号", "示数类型", "上次表示数", "本次表示数",
    "倍率", "抄见电量（千瓦时)", "换表电量（千瓦时)",
    "变/线损电量（千瓦时)", "合计电量（千瓦时)"
])

# 创建一个列表来存储所有提取的数据
data_list = []

# 遍历PDF文件夹并提取数据
for filename in os.listdir(pdf_folder_path):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder_path, filename)
        data = extract_data_from_pdf(pdf_path, filename)  # 传递文件名
        # 将多行数据添加到data_list中
        for i in range(len(data["表计资产编号"])):
            row = {
                "文件名": data["文件名"],
                "用户编号": data["用户编号"],
                "市场化属性分类": data["市场化属性分类"],
                "应缴电费合计金额": data["应缴电费合计金额"],
                "用电地址": data["用电地址"],
                "表计资产编号": data["表计资产编号"][i],
                "示数类型": data["示数类型"][i],
                "上次表示数": data["上次表示数"][i],
                "本次表示数": data["本次表示数"][i],
                "倍率": data["倍率"][i],
                "抄见电量（千瓦时)": data["抄见电量（千瓦时)"][i],
                "换表电量（千瓦时)": data["换表电量（千瓦时)"][i],
                "变/线损电量（千瓦时)": data["变/线损电量（千瓦时)"][i],
                "合计电量（千瓦时)": data["合计电量（千瓦时)"][i],
            }
            data_list.append(row)

# 将数据列表转换为DataFrame
df = pd.DataFrame(data_list)

# 保存到Excel
output_excel_path = os.path.join(pdf_folder_path, "extracted_data.xlsx")
df.to_excel(output_excel_path, index=False)

print(f"数据已成功提取并保存到 {output_excel_path}")

