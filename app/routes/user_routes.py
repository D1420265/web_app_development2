from flask import Blueprint, render_template, request, redirect, url_for, flash
# from app.models import CollectionModel

user_bp = Blueprint('user', __name__)

@user_bp.route('/collections')
def collection_list():
    """個人單字本：顯示使用者收藏的所有單字"""
    pass

@user_bp.route('/collections', methods=['POST'])
def add_to_collection():
    """加入收藏：接收 word_id，將單字加入個人單字本"""
    pass

@user_bp.route('/collections/<int:id>/delete', methods=['POST'])
def remove_from_collection(id):
    """移除收藏：將單字從個人單字本中移除"""
    pass

@user_bp.route('/quiz')
def quiz():
    """單字測驗：隨機抽取單字供使用者進行測驗"""
    pass
