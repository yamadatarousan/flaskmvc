# app/__init__.py
from flask import Flask, render_template, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import logging

# グローバル変数として宣言
db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # URLの末尾スラッシュを無視する設定
    app.url_map.strict_slashes = False
    
    # ログ設定
    if app.debug:
        logging.basicConfig(level=logging.DEBUG)
        app.logger.setLevel(logging.DEBUG)
    
    # 拡張機能の初期化
    db.init_app(app)
    csrf.init_app(app)

    # ルーティング設定
    from app.controllers import user_controller
    from app.controllers.task_controller import task_bp
    from app.controllers.profile_controller import profile_bp
    app.register_blueprint(user_controller.bp)
    app.register_blueprint(user_controller.root_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(profile_bp)
    
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