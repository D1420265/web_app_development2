# 路由設計 - 英文單字系統

本文件定義系統中所有的 URL 路由（Routes）以及與前端 Jinja2 模板的對應關係。所有路由設計皆盡可能符合 RESTful 慣例。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|---|---|---|---|---|
| 首頁 (單字列表) | GET | `/` | `index.html` | 顯示所有已建立的單字 |
| 查詢單字 | GET | `/search` | `index.html` | 透過 `?q=` 查詢單字並顯示結果 |
| 新增單字頁面 | GET | `/words/new` | `add_word.html` | 顯示新增單字的表單 |
| 建立單字 | POST | `/words` | — | 接收表單，新增至資料庫後重導向至 `/` |
| 刪除單字 | POST | `/words/<int:id>/delete`| — | 刪除單字後重導向至 `/` |
| 個人單字本 | GET | `/collections` | `collection.html` | 顯示使用者收藏的單字 |
| 加入收藏 | POST | `/collections` | — | 接收 `word_id` 加入收藏，重導向至原頁面 |
| 移除收藏 | POST | `/collections/<int:id>/delete`| — | 從收藏中移除，重導向至 `/collections` |
| 單字測驗 | GET | `/quiz` | `quiz.html` | 隨機產生題目進行測驗 |

## 2. 路由詳細說明

### 2.1 核心單字功能 (`main_routes.py`)

*   **首頁 (單字列表) `/`**
    *   處理：呼叫 `WordModel.get_all()`。
    *   輸出：渲染 `index.html`，傳遞 `words` 變數。
*   **查詢單字 `/search`**
    *   輸入：URL 參數 `q` (搜尋字串)。
    *   處理：檢查 `q`，若有則呼叫 `WordModel.search(q)`。
    *   輸出：渲染 `index.html`，傳遞 `words` 與 `query` 變數。
*   **新增單字頁面 `/words/new`**
    *   輸出：渲染 `add_word.html`。
*   **建立單字 `/words` (POST)**
    *   輸入：表單欄位 `english`, `chinese`。
    *   處理：驗證必填欄位，呼叫 `WordModel.create()`。
    *   輸出：成功後使用 Flash 訊息提示，並重導向至 `/`。
*   **刪除單字 `/words/<id>/delete` (POST)**
    *   輸入：URL 變數 `id`。
    *   處理：呼叫 `WordModel.delete(id)`。
    *   輸出：重導向至 `/`。

### 2.2 使用者收藏與測驗 (`user_routes.py`)

*   **個人單字本 `/collections`**
    *   處理：呼叫 `CollectionModel.get_all()`。
    *   輸出：渲染 `collection.html`，傳遞 `collections` 變數。
*   **加入收藏 `/collections` (POST)**
    *   輸入：表單欄位 `word_id`。
    *   處理：呼叫 `CollectionModel.add(word_id)`。
    *   輸出：重導向回上一頁（例如搜尋結果頁或首頁）。
*   **移除收藏 `/collections/<id>/delete` (POST)**
    *   輸入：URL 變數 `id`。
    *   處理：呼叫 `CollectionModel.remove(id)`。
    *   輸出：重導向至 `/collections`。
*   **單字測驗 `/quiz`**
    *   處理：呼叫 `CollectionModel.get_random_words(limit=10)`。
    *   輸出：渲染 `quiz.html`，傳遞 `quiz_words` 變數。

## 3. Jinja2 模板清單

所有的模板檔案將放置於 `app/templates/` 目錄下，且均繼承自 `base.html`，以確保全站風格一致。

1.  **`base.html`**：全站共用骨架（包含網站標題、導覽列 Navigation、Flash 錯誤/成功訊息顯示區域）。
2.  **`index.html`**：用於首頁與搜尋結果，以表格或清單方式列出單字，每列有「加入收藏」按鈕。
3.  **`add_word.html`**：新增單字表單，包含兩個輸入框（英文、中文）與提交按鈕。
4.  **`collection.html`**：個人單字本頁面，列出已收藏的單字，並有「移除收藏」按鈕。
5.  **`quiz.html`**：單字測驗頁面，展示隨機抽取的單字供使用者互動作答。
