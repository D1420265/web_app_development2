from .db import get_db_connection

class CollectionModel:
    @staticmethod
    def get_all():
        """取得所有收藏的單字與翻譯，包含 JOIN 的結果"""
        with get_db_connection() as conn:
            return conn.execute("""
                SELECT c.id as collection_id, c.created_at as collected_at, w.* 
                FROM collections c 
                JOIN words w ON c.word_id = w.id 
                ORDER BY c.created_at DESC
            """).fetchall()

    @staticmethod
    def add(word_id):
        """將單字加入收藏庫，如果已存在則不重複新增"""
        with get_db_connection() as conn:
            # 檢查是否已收藏
            existing = conn.execute("SELECT id FROM collections WHERE word_id = ?", (word_id,)).fetchone()
            if existing:
                return existing['id']
            
            cursor = conn.cursor()
            cursor.execute("INSERT INTO collections (word_id) VALUES (?)", (word_id,))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def remove(collection_id):
        """將單字從收藏庫中移除"""
        with get_db_connection() as conn:
            conn.execute("DELETE FROM collections WHERE id = ?", (collection_id,))
            conn.commit()

    @staticmethod
    def get_random_words(limit=10):
        """隨機取得收藏庫中的單字供測驗使用"""
        with get_db_connection() as conn:
            return conn.execute("""
                SELECT w.* FROM words w
                JOIN collections c ON w.id = c.word_id
                ORDER BY RANDOM() LIMIT ?
            """, (limit,)).fetchall()
