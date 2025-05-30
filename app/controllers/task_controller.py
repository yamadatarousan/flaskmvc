from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.task import Task
from app.models.user import User
from app.forms.task_form import TaskForm
from sqlalchemy import or_, and_
from datetime import datetime

task_bp = Blueprint('task', __name__)

@task_bp.route('/tasks')
@login_required
def task_list():
    """タスク一覧表示"""
    # 検索・フィルタリングパラメータを取得
    search_query = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    user_filter = request.args.get('user', '')
    due_date_filter = request.args.get('due_date', '')
    sort_by = request.args.get('sort', 'created_at')
    order = request.args.get('order', 'desc')
    
    # ベースクエリ
    query = Task.query.join(User)
    
    # 検索条件を適用
    if search_query:
        search_pattern = f"%{search_query}%"
        query = query.filter(
            or_(
                Task.title.ilike(search_pattern),
                Task.description.ilike(search_pattern),
                User.name.ilike(search_pattern)
            )
        )
    
    # ステータスフィルター
    if status_filter:
        query = query.filter(Task.status == status_filter)
    
    # ユーザーフィルター
    if user_filter:
        query = query.filter(Task.user_id == user_filter)
    
    # 期限フィルター
    if due_date_filter:
        today = datetime.now().date()
        if due_date_filter == 'overdue':
            query = query.filter(and_(Task.due_date < today, Task.status != 'completed'))
        elif due_date_filter == 'today':
            query = query.filter(Task.due_date == today)
        elif due_date_filter == 'this_week':
            from datetime import timedelta
            week_end = today + timedelta(days=7)
            query = query.filter(and_(Task.due_date >= today, Task.due_date <= week_end))
    
    # ソート条件を適用
    if sort_by == 'title':
        if order == 'desc':
            query = query.order_by(Task.title.desc())
        else:
            query = query.order_by(Task.title.asc())
    elif sort_by == 'status':
        if order == 'desc':
            query = query.order_by(Task.status.desc())
        else:
            query = query.order_by(Task.status.asc())
    elif sort_by == 'due_date':
        if order == 'desc':
            query = query.order_by(Task.due_date.desc())
        else:
            query = query.order_by(Task.due_date.asc())
    elif sort_by == 'user':
        if order == 'desc':
            query = query.order_by(User.name.desc())
        else:
            query = query.order_by(User.name.asc())
    else:  # created_at
        if order == 'desc':
            query = query.order_by(Task.created_at.desc())
        else:
            query = query.order_by(Task.created_at.asc())
    
    tasks = query.all()
    users_for_filter = User.query.all()
    total_count = Task.query.count()
    filtered_count = len(tasks)
    
    # 各タスクに日付状態を追加
    today = datetime.now().date()
    for task in tasks:
        if task.due_date:
            if task.due_date < today and task.status != 'completed':
                task.date_status = 'overdue'
            elif task.due_date == today:
                task.date_status = 'today'
            else:
                task.date_status = 'normal'
        else:
            task.date_status = 'none'
    
    # ステータス統計
    status_counts = {
        'pending': Task.query.filter_by(status='pending').count(),
        'in_progress': Task.query.filter_by(status='in_progress').count(),
        'completed': Task.query.filter_by(status='completed').count()
    }
    
    return render_template('task_list.html', 
                         tasks=tasks,
                         users_for_filter=users_for_filter,
                         search_query=search_query,
                         status_filter=status_filter,
                         user_filter=user_filter,
                         due_date_filter=due_date_filter,
                         sort_by=sort_by,
                         order=order,
                         total_count=total_count,
                         filtered_count=filtered_count,
                         status_counts=status_counts)

@task_bp.route('/tasks/create', methods=['GET', 'POST'])
@login_required
def create_task():
    """タスク新規作成"""
    form = TaskForm()
    users = User.query.all()
    
    # SelectFieldの選択肢を設定
    form.user_id.choices = [('', '担当者を選択してください')] + [(user.id, user.name) for user in users]
    
    if form.validate_on_submit():
        try:
            task = Task(
                title=form.title.data,
                description=form.description.data,
                status=form.status.data,
                due_date=form.due_date.data,
                user_id=form.user_id.data
            )
            db.session.add(task)
            db.session.commit()
            flash('タスクが正常に作成されました。', 'success')
            return redirect(url_for('task.task_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'タスクの作成中にエラーが発生しました: {str(e)}', 'error')
    
    return render_template('task_form.html', form=form, users=users, action='新規作成')

@task_bp.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    """タスク編集"""
    task = Task.query.get_or_404(task_id)
    form = TaskForm(obj=task)
    users = User.query.all()
    
    # SelectFieldの選択肢を設定
    form.user_id.choices = [('', '担当者を選択してください')] + [(user.id, user.name) for user in users]
    
    if form.validate_on_submit():
        try:
            task.title = form.title.data
            task.description = form.description.data
            task.status = form.status.data
            task.due_date = form.due_date.data
            task.user_id = form.user_id.data
            db.session.commit()
            flash('タスクが正常に更新されました。', 'success')
            return redirect(url_for('task.task_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'タスクの更新中にエラーが発生しました: {str(e)}', 'error')
    
    return render_template('task_form.html', form=form, users=users, task=task, action='編集')

@task_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    """タスク削除"""
    task = Task.query.get_or_404(task_id)
    
    try:
        db.session.delete(task)
        db.session.commit()
        flash('タスクが正常に削除されました。', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'タスクの削除中にエラーが発生しました: {str(e)}', 'error')
    
    return redirect(url_for('task.task_list'))

@task_bp.route('/tasks/<int:task_id>')
@login_required
def task_detail(task_id):
    """タスク詳細表示"""
    task = Task.query.get_or_404(task_id)
    return render_template('task_detail.html', task=task) 