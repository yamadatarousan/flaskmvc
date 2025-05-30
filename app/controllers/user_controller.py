# app/controllers/user_controller.py
from flask import Blueprint, render_template, current_app, request, redirect, url_for, flash
from flask_login import login_required
from app.models.user import User
from app.forms.user_form import UserForm
from app import db
import logging

# ログ設定
logger = logging.getLogger(__name__)

bp = Blueprint('user', __name__, url_prefix='/users')

@bp.route('/')
@bp.route('')
@login_required
def list_users():
    try:
        logger.info("Accessing user list route")
        users = User.query.all()
        logger.info(f"Found {len(users)} users")
        return render_template('user_list.html', users=users)
    except Exception as e:
        logger.error(f"Error in list_users: {e}")
        return render_template('error.html', error=str(e)), 500

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_user():
    """新規ユーザー作成"""
    form = UserForm()
    if form.validate_on_submit():
        try:
            user = User(name=form.name.data, email=form.email.data)
            user.set_password('password123')  # デフォルトパスワードを設定
            db.session.add(user)
            db.session.commit()
            flash('ユーザーが作成されました', 'success')
            return redirect(url_for('user.list_users'))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating user: {e}")
            flash(f'ユーザー作成中にエラーが発生しました: {e}', 'danger')
    
    return render_template('user_form.html', form=form, action='create')

@bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    """ユーザー編集"""
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    
    if request.method == 'GET':
        # GETリクエスト時にフォームにデータを設定
        form.id.data = user.id
    
    if form.validate_on_submit():
        try:
            user.name = form.name.data
            user.email = form.email.data
            db.session.commit()
            flash('ユーザーが更新されました', 'success')
            return redirect(url_for('user.list_users'))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating user: {e}")
            flash(f'ユーザー更新中にエラーが発生しました: {e}', 'danger')
    
    return render_template('user_form.html', form=form, user=user, action='edit')

@bp.route('/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    """ユーザー削除"""
    user = User.query.get_or_404(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
        flash('ユーザーが削除されました', 'success')
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting user: {e}")
        flash(f'ユーザー削除中にエラーが発生しました: {e}', 'danger')
    
    return redirect(url_for('user.list_users'))

# ルートURL用に新しいブループリントを作成
root_bp = Blueprint('root', __name__)

@root_bp.route('/')
def index():
    """ホームページ - ログイン不要"""
    try:
        logger.info("Accessing root index route")
        return render_template('home.html')
    except Exception as e:
        logger.error(f"Error in index: {e}")
        return render_template('error.html', error=str(e)), 500