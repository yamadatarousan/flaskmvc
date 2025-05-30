# Flask MVC Application

本プロジェクトは、Laravel風のMVC（Model-View-Controller）アーキテクチャを採用したFlaskウェブアプリケーションです。

## 🚀 機能概要

### 認証システム
- ユーザー登録・ログイン・ログアウト
- セッション管理（Flask-Login）
- パスワードハッシュ化（Werkzeug Security）

### CRUD機能
- **ユーザー管理**: ユーザーの作成、表示、編集、削除
- **タスク管理**: タスクの作成、表示、編集、削除（ステータス管理付き）
- **プロフィール管理**: ユーザープロフィールの管理（住所、電話番号等）

### システム機能
- Laravel風統一ログシステム
- Bootstrap 5 による現代的なUI
- レスポンシブデザイン
- バリデーション機能
- エラーハンドリング

## 🛠️ 技術スタック

### バックエンド
- **Flask** - Webフレームワーク
- **SQLAlchemy** - ORM
- **Flask-Login** - 認証管理
- **Flask-WTF** - フォーム処理・バリデーション
- **Werkzeug** - パスワードハッシュ化

### フロントエンド
- **Bootstrap 5** - CSSフレームワーク
- **Jinja2** - テンプレートエンジン

### データベース
- **MySQL** - データベース
- **PyMySQL** - MySQLドライバー

## 📁 プロジェクト構造

```
flaskmvc/
├── app/
│   ├── __init__.py              # アプリケーション初期化
│   ├── models/                  # データモデル
│   │   ├── __init__.py
│   │   ├── user.py             # Userモデル
│   │   ├── task.py             # Taskモデル
│   │   └── profile.py          # Profileモデル
│   ├── controllers/             # コントローラー
│   │   ├── user_controller.py  # ユーザー管理
│   │   ├── task_controller.py  # タスク管理
│   │   ├── profile_controller.py # プロフィール管理
│   │   └── auth_controller.py  # 認証処理
│   ├── forms/                   # フォーム定義
│   │   ├── __init__.py
│   │   ├── user_form.py
│   │   ├── task_form.py
│   │   ├── profile_form.py
│   │   └── auth_forms.py
│   ├── templates/               # HTMLテンプレート
│   │   ├── layout.html         # ベースレイアウト
│   │   ├── home.html           # ホームページ
│   │   ├── users/              # ユーザー関連
│   │   ├── tasks/              # タスク関連
│   │   ├── profiles/           # プロフィール関連
│   │   └── auth/               # 認証関連
│   └── utils/                   # ユーティリティ
│       └── __init__.py         # Laravel風ログ機能
├── storage/
│   └── logs/
│       └── flask.log           # アプリケーションログ
├── config.py                    # 設定ファイル
├── run.py                      # アプリケーション起動
└── requirements.txt            # 依存関係
```

## 🔧 セットアップ

### 前提条件
- Python 3.8+
- MySQL 8.0+

### 1. プロジェクトのクローン
```bash
git clone <repository-url>
cd flaskmvc
```

### 2. 仮想環境の作成
```bash
python -m venv myenv
source myenv/bin/activate  # macOS/Linux
# myenv\Scripts\activate   # Windows
```

### 3. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 4. データベースの設定
MySQLで新しいデータベースを作成：
```sql
CREATE DATABASE flaskmvc CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. 設定ファイルの編集
`config.py` で以下を適切に設定：
```python
# データベース設定
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/flaskmvc'

# セキュリティ設定
SECRET_KEY = 'your-secret-key-here'
```

### 6. データベーステーブルの作成
```bash
python run.py
```
初回起動時に自動的にテーブルとテストデータが作成されます。

## 🚀 起動方法

```bash
python run.py
```

アプリケーションは `http://localhost:5001` で起動します。

## 📊 データモデル

### User (ユーザー)
- `id`: 主キー
- `name`: ユーザー名
- `email`: メールアドレス（ユニーク）
- `password_hash`: ハッシュ化されたパスワード
- `created_at`, `updated_at`: タイムスタンプ

### Task (タスク)
- `id`: 主キー
- `title`: タスク名
- `description`: 説明
- `status`: ステータス（pending/in_progress/completed）
- `due_date`: 期限日
- `user_id`: ユーザーID（外部キー）
- `created_at`, `updated_at`: タイムスタンプ

### Profile (プロフィール)
- `id`: 主キー
- `user_id`: ユーザーID（外部キー、1対1関係）
- `birth_date`: 生年月日
- `address`: 住所
- `phone_number`: 電話番号
- `created_at`, `updated_at`: タイムスタンプ

## 🎨 UI機能

### 認証
- ログインフォーム（メールアドレス、パスワード、記憶する）
- ユーザー登録フォーム（名前、メールアドレス、パスワード確認）
- ログアウト機能

### ナビゲーション
- レスポンシブナビゲーションバー
- ドロップダウンメニュー
- ログイン状態に応じた表示切り替え

### データ管理
- テーブル形式のデータ表示
- 作成・編集・削除ボタン
- 削除確認モーダル
- バリデーションエラー表示
- フラッシュメッセージ

## 📝 Laravel風ログ機能

### 使用方法
```python
from app.utils import log_info, log_error, log_warning, log_debug

# 情報ログ
log_info("ユーザーが正常に作成されました")

# エラーログ
log_error(f"データベースエラー: {e}")

# 警告ログ
log_warning("不正なアクセスを検出しました")

# デバッグログ
log_debug("デバッグ情報")
```

### ログファイル
ログは `storage/logs/flask.log` に出力され、以下の情報が記録されます：
- タイムスタンプ
- ログレベル
- 実際の呼び出し元ファイルと行番号
- メッセージ内容

### ログローテーション
- ファイルサイズ上限: 10MB
- バックアップファイル数: 5個
- 自動ローテーション機能

## 🔒 セキュリティ機能

### 認証・認可
- ログイン必須ページの保護（`@login_required`）
- セッション管理
- CSRF保護（Flask-WTF）

### データ保護
- パスワードハッシュ化
- SQLインジェクション対策（SQLAlchemy ORM）
- XSS対策（Jinja2自動エスケープ）

## 🎯 主要な機能

### ユーザー管理
- 一覧表示、作成、編集、削除
- メールアドレスの重複チェック
- 関連データの連鎖削除

### タスク管理
- ステータス管理（pending/in_progress/completed）
- 期限日設定
- ユーザーごとのタスク管理

### プロフィール管理
- ユーザーとの1対1関係
- 電話番号バリデーション
- 重複プロフィール防止

## 🚨 エラーハンドリング

- 包括的なtry-catch文
- ユーザーフレンドリーなエラーメッセージ
- 詳細なログ記録
- 適切なHTTPステータスコード

## 📋 開発時の注意事項

### ポート設定
- デフォルトポート: 5001（macOS AirPlayとの競合回避）
- 変更が必要な場合は `run.py` を編集

### ログ設定
- 開発環境: DEBUG レベル
- 本番環境: INFO レベル以上を推奨

### データベース
- 初回起動時にテストデータが自動作成
- 本番環境では `create_test_data()` を無効化推奨

## 🤝 貢献

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add some amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. Pull Requestを作成

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 🙋‍♂️ サポート

質問やイシューがある場合は、GitHubのIssuesページでお知らせください。
