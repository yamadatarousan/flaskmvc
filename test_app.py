from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>テスト</title>
    </head>
    <body>
        <h1>テストページ</h1>
        <p>これはテストページです。</p>
        <p><a href="/users">ユーザー一覧へ</a></p>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/users')
@app.route('/users/')
def users():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ユーザー一覧</title>
    </head>
    <body>
        <h1>ユーザー一覧</h1>
        <p>これはユーザー一覧のテストページです。</p>
        <p><a href="/">トップへ戻る</a></p>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True, port=5001) 