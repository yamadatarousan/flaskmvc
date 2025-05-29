from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.task import Task
from app.models.user import User
from app.forms.task_form import TaskForm

task_bp = Blueprint('task', __name__)

@task_bp.route('/tasks')
def task_list():
    """タスク一覧表示"""
    tasks = Task.query.join(User).all()
    return render_template('task_list.html', tasks=tasks)

@task_bp.route('/tasks/create', methods=['GET', 'POST'])
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
def task_detail(task_id):
    """タスク詳細表示"""
    task = Task.query.get_or_404(task_id)
    return render_template('task_detail.html', task=task) 