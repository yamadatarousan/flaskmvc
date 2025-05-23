# run.py
import sys
import logging
print(sys.path)
from app import create_app, db
from app.models.user import User

app = create_app()

# ロギングを詳細に設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('werkzeug')
logger.setLevel(logging.DEBUG)

with app.app_context():
    db.create_all()  # テーブル作成
    # テストデータ追加（既にデータがある場合はスキップ）
    if not User.query.first():  # テーブルが空の場合のみ追加
        users = [
            User(name="Alice", email="alice@example.com"),
            User(name="Bob", email="bob@example.com")
        ]
        db.session.add_all(users)
        db.session.commit()
        print("Test data added.")

if __name__ == '__main__':
    # ポート5001を使用して実行
    app.run(debug=True, port=5001)