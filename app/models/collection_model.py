import sqlite3
from .db import get_db_connection

class CollectionModel:
    @staticmethod
    def get_all():
        """取得所有收藏的單字與翻譯，包含 JOIN 的結果"""
        try:
            with get_db_connection() as conn:
                return conn.execute("""
                    SELECT c.id as collection_id, c.created_at as collected_at, w.* 
                    FROM collections c 
                    JOIN words w ON c.word_id = w.id 
                    ORDER BY c.created_at DESC
                """).fetchall()
        except sqlite3.Error as e:
            print(f"Database error in get_all: {e}")
            return []

    @staticmethod
    def get_by_id(collection_id):
        """依據 ID 取得單筆收藏紀錄"""
        try:
            with get_db_connection() as conn:
                return conn.execute("""
                    SELECT c.id as collection_id, c.created_at as collected_at, w.* 
                    FROM collections c 
                    JOIN words w ON c.word_id = w.id 
                    WHERE c.id = ?
                """, (collection_id,)).fetchone()
        except sqlite3.Error as e:
            print(f"Database error in get_by_id: {e}")
            return None

    @staticmethod
    def add(word_id):
        """將單字加入收藏庫，如果已存在則不重複新增"""
        try:
            with get_db_connection() as conn:
                # 檢查是否已收藏
                existing = conn.execute("SELECT id FROM collections WHERE word_id = ?", (word_id,)).fetchone()
                if existing:
                    return existing['id']
                
                cursor = conn.cursor()
                cursor.execute("INSERT INTO collections (word_id) VALUES (?)", (word_id,))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error in add: {e}")
            return None

    @staticmethod
    def update(collection_id, word_id):
        """更新收藏紀錄 (在當前 MVP 較少用到，但為了介面完整性實作)"""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE collections SET word_id = ? WHERE id = ?",
                    (word_id, collection_id)
                )
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error in update: {e}")
            return False

    @staticmethod
    def remove(collection_id):
        """將單字從收藏庫中移除"""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM collections WHERE id = ?", (collection_id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error in remove: {e}")
            return False

    @staticmethod
    def get_random_words(limit=10):
        """隨機取得收藏庫中的單字供測驗使用"""
        try:
            with get_db_connection() as conn:
                return conn.execute("""
                    SELECT w.* FROM words w
                    JOIN collections c ON w.id = c.word_id
                    ORDER BY RANDOM() LIMIT ?
                """, (limit,)).fetchall()
        except sqlite3.Error as e:
            print(f"Database error in get_random_words: {e}")
            return []
