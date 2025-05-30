from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User
from app.forms.login_form import LoginForm, RegistrationForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """ログイン"""
    if current_user.is_authenticated:
        return redirect(url_for('root.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('root.index')
            flash('ログインしました。', 'success')
            return redirect(next_page)
        else:
            flash('メールアドレスまたはパスワードが正しくありません。', 'error')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """ログアウト"""
    logout_user()
    flash('ログアウトしました。', 'info')
    return redirect(url_for('root.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """ユーザー登録"""
    if current_user.is_authenticated:
        return redirect(url_for('root.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = User(
                name=form.name.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('ユーザー登録が完了しました。ログインしてください。', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'ユーザー登録中にエラーが発生しました: {str(e)}', 'error')
    
    return render_template('auth/register.html', form=form) 