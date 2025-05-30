# app/__init__.py
from flask import Flask, render_template, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import logging
from logging.handlers import RotatingFileHandler
import os
from flask_login import LoginManager
from config import Config

# グローバル変数として宣言
db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()

def setup_logging(app):
    """ログ設定のセットアップ"""
    if not app.debug and not app.testing:
        # 本番環境用のログ設定
        log_level = getattr(logging, app.config.get('LOG_LEVEL', 'INFO'))
    else:
        # 開発環境用のログ設定
        log_level = logging.DEBUG
    
    # ログディレクトリの作成
    log_dir = app.config.get('LOG_DIR')
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # ファイルハンドラーの設定
    if log_dir:
        file_handler = RotatingFileHandler(
            app.config.get('LOG_FILE'),
            maxBytes=app.config.get('LOG_MAX_BYTES', 10*1024*1024),
            backupCount=app.config.get('LOG_BACKUP_COUNT', 5),
            encoding='utf-8'
        )
        file_handler.setLevel(log_level)
        
        # ログフォーマットの設定
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s (%(pathname)s:%(lineno)d): %(message)s'
        )
        file_handler.setFormatter(formatter)
        
        # アプリのロガーに追加
        app.logger.addHandler(file_handler)
        app.logger.setLevel(log_level)
        
        # Werkzeug（Flask内部）のログも同じファイルに出力
        werkzeug_logger = logging.getLogger('werkzeug')
        werkzeug_logger.addHandler(file_handler)
        werkzeug_logger.setLevel(log_level)
        
        # SQLAlchemyのログも追加
        sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
        if app.debug:
            sqlalchemy_logger.addHandler(file_handler)
            sqlalchemy_logger.setLevel(logging.INFO)
    
    # コンソール出力の設定
    if not app.logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        app.logger.addHandler(console_handler)
        app.logger.setLevel(log_level)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # ログ設定のセットアップ
    setup_logging(app)
    
    # 初期化
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'ログインが必要です。'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))

    # ルーティング設定
    from app.controllers import user_controller
    from app.controllers.task_controller import task_bp
    from app.controllers.profile_controller import profile_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.dashboard_controller import dashboard_bp
    app.register_blueprint(user_controller.bp)
    app.register_blueprint(user_controller.root_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    
    # シンプルなテストルート
    @app.route('/test')
    def test():
        return render_template('user_list.html', users=[])
    
    # デバッグ用のルート
    @app.route('/debug')
    def debug():
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>デバッグ</title>
        </head>
        <body>
            <h1>デバッグページ</h1>
            <p>これはデバッグ用のページです。このページが表示されれば、Flaskは正常に動作しています。</p>
        </body>
        </html>
        """
        return render_template_string(html)
    
    # エラーハンドラーの登録
    @app.errorhandler(403)
    def forbidden_error(error):
        app.logger.error(f"403 Error: {error}")
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>403 エラー</title>
        </head>
        <body>
            <h1>403 Forbidden</h1>
            <p>アクセスが拒否されました: {error}</p>
        </body>
        </html>
        """, 403
        
    @app.errorhandler(404)
    def not_found_error(error):
        app.logger.error(f"404 Error: {error}")
        return render_template('error.html', error="ページが見つかりません。"), 404
        
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"500 Error: {error}")
        db.session.rollback()
        return render_template('error.html', error="内部サーバーエラーが発生しました。"), 500

    return app