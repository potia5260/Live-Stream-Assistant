import re
from pathlib import Path


def natural_sort_key(filename: str):
    """生成自然排序的键值"""
    # 使用正则表达式拆分数字和非数字部分
    parts = re.split(r'(\d+)', filename)
    # 将数字部分转为整数，其他保持字符串
    return [
        int(part) if part.isdigit() else part.lower()
        for part in parts
    ]
