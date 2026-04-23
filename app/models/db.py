import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """建立並回傳資料庫連線"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    # 將查詢結果從 Tuple 轉換為類似 dict 的 Row 物件，方便透過欄位名稱取值
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化資料庫與資料表結構"""
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    os.makedirs(os.path.dirname(schema_path), exist_ok=True)
    
    if os.path.exists(schema_path):
        with get_db_connection() as conn:
            with open(schema_path, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
            conn.commit()
