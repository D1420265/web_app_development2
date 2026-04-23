import os
from flask import Flask
from .models.db import init_db

def create_app(test_config=None):
    # 建立並設定 Flask App
    app = Flask(__name__, instance_relative_config=True)
    
    # 基本設定
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev_secret_key_for_local_testing'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # 確保 instance 資料夾存在 (用來放 database.db)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 初始化資料庫
    with app.app_context():
        init_db()

    # 註冊 Blueprints (路由模組)
    from .routes.main_routes import main_bp
    from .routes.user_routes import user_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)

    return app
