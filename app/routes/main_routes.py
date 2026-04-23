from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.word_model import WordModel

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """首頁：顯示所有單字列表"""
    words = WordModel.get_all()
    return render_template('index.html', words=words)

@main_bp.route('/search')
def search():
    """查詢單字：透過 ?q= 參數進行搜尋，顯示結果"""
    query = request.args.get('q', '').strip()
    if query:
        words = WordModel.search(query)
    else:
        words = WordModel.get_all()
    return render_template('index.html', words=words, query=query)

@main_bp.route('/words/new')
def new_word():
    """新增單字頁面：顯示輸入表單"""
    return render_template('add_word.html')

@main_bp.route('/words', methods=['POST'])
def create_word():
    """建立單字：接收表單資料，寫入資料庫後重導向至首頁"""
    english = request.form.get('english', '').strip()
    chinese = request.form.get('chinese', '').strip()
    
    # 基礎輸入驗證
    if not english or not chinese:
        flash('英文單字與中文翻譯皆為必填！', 'danger')
        return redirect(url_for('main.new_word'))
        
    # 呼叫 Model 寫入資料
    word_id = WordModel.create(english, chinese)
    
    if word_id:
        flash('單字新增成功！', 'success')
        return redirect(url_for('main.index'))
    else:
        flash('單字新增失敗，請稍後再試。', 'danger')
        return redirect(url_for('main.new_word'))

@main_bp.route('/words/<int:id>/delete', methods=['POST'])
def delete_word(id):
    """刪除單字：將單字從資料庫徹底刪除"""
    success = WordModel.delete(id)
    if success:
        flash('單字已成功刪除！', 'success')
    else:
        flash('刪除失敗或單字不存在。', 'danger')
    return redirect(url_for('main.index'))
