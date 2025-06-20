# app/controllers/user_controller.py
from flask import Blueprint, render_template, current_app, request, redirect, url_for, flash
from flask_login import login_required
from app.models.user import User
from app.forms.user_form import UserForm
from app import db
from app.utils import log_info, log_error
from sqlalchemy import or_

bp = Blueprint('user', __name__, url_prefix='/users')

@bp.route('/')
@bp.route('')
@login_required
def list_users():
    try:
        log_info("Accessing user list route from user_controller")
        
        # 検索パラメータを取得
        search_query = request.args.get('search', '')
        sort_by = request.args.get('sort', 'name')
        order = request.args.get('order', 'asc')
        
        # ベースクエリ
        query = User.query
        
        # 検索条件を適用
        if search_query:
            search_pattern = f"%{search_query}%"
            query = query.filter(
                or_(
                    User.name.ilike(search_pattern),
                    User.email.ilike(search_pattern)
                )
            )
        
        # ソート条件を適用
        if sort_by == 'name':
            if order == 'desc':
                query = query.order_by(User.name.desc())
            else:
                query = query.order_by(User.name.asc())
        elif sort_by == 'email':
            if order == 'desc':
                query = query.order_by(User.email.desc())
            else:
                query = query.order_by(User.email.asc())
        elif sort_by == 'created_at':
            if order == 'desc':
                query = query.order_by(User.created_at.desc())
            else:
                query = query.order_by(User.created_at.asc())
        
        users = query.all()
        total_count = User.query.count()
        filtered_count = len(users)
        
        log_info(f"Found {filtered_count}/{total_count} users with search: '{search_query}'")
        
        return render_template('user_list.html', 
                             users=users,
                             search_query=search_query,
                             sort_by=sort_by,
                             order=order,
                             total_count=total_count,
                             filtered_count=filtered_count)
    except Exception as e:
        log_error(f"Error in list_users: {e}")
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
            log_info(f"User created: {user.name} ({user.email})")
            flash('ユーザーが作成されました', 'success')
            return redirect(url_for('user.list_users'))
        except Exception as e:
            db.session.rollback()
            log_error(f"Error creating user: {e}")
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
            old_name = user.name
            user.name = form.name.data
            user.email = form.email.data
            db.session.commit()
            log_info(f"User updated: {old_name} -> {user.name} ({user.email})")
            flash('ユーザーが更新されました', 'success')
            return redirect(url_for('user.list_users'))
        except Exception as e:
            db.session.rollback()
            log_error(f"Error updating user: {e}")
            flash(f'ユーザー更新中にエラーが発生しました: {e}', 'danger')
    
    return render_template('user_form.html', form=form, user=user, action='edit')

@bp.route('/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    """ユーザー削除"""
    user = User.query.get_or_404(user_id)
    try:
        user_name = user.name
        db.session.delete(user)
        db.session.commit()
        log_info(f"User deleted: {user_name}")
        flash('ユーザーが削除されました', 'success')
    except Exception as e:
        db.session.rollback()
        log_error(f"Error deleting user: {e}")
        flash(f'ユーザー削除中にエラーが発生しました: {e}', 'danger')
    
    return redirect(url_for('user.list_users'))

# ルートURL用に新しいブループリントを作成
root_bp = Blueprint('root', __name__)

@root_bp.route('/')
def index():
    """ホームページ - ログイン不要"""
    try:
        log_info("Accessing root index route from user_controller.py")
        return render_template('home.html')
    except Exception as e:
        log_error(f"Error in index: {e}")
        return render_template('error.html', error=str(e)), 500