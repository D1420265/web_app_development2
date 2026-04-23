from .db import get_db_connection

class WordModel:
    @staticmethod
    def get_all():
        """取得所有單字，依建立時間反序排列"""
        with get_db_connection() as conn:
            return conn.execute("SELECT * FROM words ORDER BY created_at DESC").fetchall()

    @staticmethod
    def get_by_id(word_id):
        """依據 ID 取得單筆單字"""
        with get_db_connection() as conn:
            return conn.execute("SELECT * FROM words WHERE id = ?", (word_id,)).fetchone()

    @staticmethod
    def search(keyword):
        """模糊搜尋英文或中文包含關鍵字的單字"""
        with get_db_connection() as conn:
            query = f"%{keyword}%"
            return conn.execute(
                "SELECT * FROM words WHERE english LIKE ? OR chinese LIKE ? ORDER BY created_at DESC", 
                (query, query)
            ).fetchall()

    @staticmethod
    def create(english, chinese):
        """新增單字，回傳新增的 ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO words (english, chinese) VALUES (?, ?)", 
                (english, chinese)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def delete(word_id):
        """刪除特定單字"""
        with get_db_connection() as conn:
            conn.execute("DELETE FROM words WHERE id = ?", (word_id,))
            conn.commit()
