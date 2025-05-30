# run.py
import sys
print(sys.path)
from app import create_app, db
from app.models.user import User
from app.models.profile import Profile
from app.models.task import Task
from datetime import date, datetime
from pprint import pprint
from app.utils import log_info

app = create_app()

with app.app_context():
    db.create_all()  # テーブル作成
    # テストデータ追加（既にデータがある場合はスキップ）
    if not User.query.first():  # テーブルが空の場合のみ追加
        log_info("Creating initial test data...")
        # ユーザーデータの作成
        users = [
            User(name="Alice", email="alice@example.com"),
            User(name="Bob", email="bob@example.com")
        ]
        # パスワードを設定
        for user in users:
            user.set_password('password123')
        
        db.session.add_all(users)
        db.session.commit()

        # プロフィールデータの作成
        profiles = [
            Profile(
                user_id=users[0].id,
                birth_date=date(1990, 1, 1),
                address="東京都渋谷区",
                phone_number="090-1234-5678"
            ),
            Profile(
                user_id=users[1].id,
                birth_date=date(1992, 5, 15),
                address="大阪府大阪市",
                phone_number="080-8765-4321"
            )
        ]
        db.session.add_all(profiles)

        # タスクデータの作成
        tasks = [
            Task(
                title="買い物リストの作成",
                description="週末の買い物に必要なものをリストアップ",
                status="pending",
                due_date=date.today(),
                user_id=users[0].id
            ),
            Task(
                title="プロジェクトの進捗報告",
                description="週次進捗報告書の作成と提出",
                status="in_progress",
                due_date=date.today(),
                user_id=users[1].id
            )
        ]
        db.session.add_all(tasks)
        db.session.commit()
        log_info("Test data created successfully")
        print("Test data added.")

if __name__ == '__main__':
    # ポート5001を使用して実行
    app.run(debug=True, port=5001)