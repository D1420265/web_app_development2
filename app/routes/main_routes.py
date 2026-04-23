from flask import Blueprint, render_template, request, redirect, url_for, flash
# from app.models import WordModel

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """首頁：顯示所有單字列表"""
    pass

@main_bp.route('/search')
def search():
    """查詢單字：透過 ?q= 參數進行搜尋，顯示結果"""
    pass

@main_bp.route('/words/new')
def new_word():
    """新增單字頁面：顯示輸入表單"""
    pass

@main_bp.route('/words', methods=['POST'])
def create_word():
    """建立單字：接收表單資料，寫入資料庫後重導向至首頁"""
    pass

@main_bp.route('/words/<int:id>/delete', methods=['POST'])
def delete_word(id):
    """刪除單字：將單字從資料庫徹底刪除"""
    pass
