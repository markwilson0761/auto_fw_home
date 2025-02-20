# app/config.py
import os

# 获取当前目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 数据库文件路径
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'data', 'firewall.db')}"
MATRIX_FILE_PATH = os.path.join(BASE_DIR, 'data', 'matrix.xlsx')
ZONE_FILE_PATH = os.path.join(BASE_DIR, 'data', 'zone.xlsx')
