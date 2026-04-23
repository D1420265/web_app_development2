import sqlite3
from .db import get_db_connection

class WordModel:
    @staticmethod
    def get_all():
        """取得所有單字，依建立時間反序排列"""
        try:
            with get_db_connection() as conn:
                return conn.execute("SELECT * FROM words ORDER BY created_at DESC").fetchall()
        except sqlite3.Error as e:
            print(f"Database error in get_all: {e}")
            return []

    @staticmethod
    def get_by_id(word_id):
        """依據 ID 取得單筆單字"""
        try:
            with get_db_connection() as conn:
                return conn.execute("SELECT * FROM words WHERE id = ?", (word_id,)).fetchone()
        except sqlite3.Error as e:
            print(f"Database error in get_by_id: {e}")
            return None

    @staticmethod
    def search(keyword):
        """模糊搜尋英文或中文包含關鍵字的單字"""
        try:
            with get_db_connection() as conn:
                query = f"%{keyword}%"
                return conn.execute(
                    "SELECT * FROM words WHERE english LIKE ? OR chinese LIKE ? ORDER BY created_at DESC", 
                    (query, query)
                ).fetchall()
        except sqlite3.Error as e:
            print(f"Database error in search: {e}")
            return []

    @staticmethod
    def create(english, chinese):
        """新增單字，回傳新增的 ID"""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO words (english, chinese) VALUES (?, ?)", 
                    (english, chinese)
                )
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error in create: {e}")
            return None

    @staticmethod
    def update(word_id, english, chinese):
        """更新單字資訊"""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE words SET english = ?, chinese = ? WHERE id = ?",
                    (english, chinese, word_id)
                )
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error in update: {e}")
            return False

    @staticmethod
    def delete(word_id):
        """刪除特定單字"""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM words WHERE id = ?", (word_id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error in delete: {e}")
            return False
