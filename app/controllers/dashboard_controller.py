from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from app.models.user import User
from app.models.task import Task
from app.models.profile import Profile
from app import db
from app.utils import log_info, log_error

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    """ダッシュボードのメイン画面"""
    try:
        log_info("Accessing dashboard from dashboard_controller")
        
        # 基本統計を取得
        stats = get_basic_statistics()
        
        # タスク統計を取得
        task_stats = get_task_statistics()
        
        # チャート用データを取得
        chart_data = get_chart_data()
        
        # 最近のアクティビティを取得
        recent_activities = get_recent_activities()
        
        log_info(f"Dashboard data loaded successfully for user {current_user.id}")
        
        return render_template('dashboard/index.html', 
                             stats=stats,
                             task_stats=task_stats,
                             chart_data=chart_data,
                             recent_activities=recent_activities)
    
    except Exception as e:
        log_error(f"Error in dashboard: {e}")
        return render_template('error.html', error=str(e)), 500

def get_basic_statistics():
    """基本統計情報を取得"""
    try:
        # 全体統計
        total_users = User.query.count()
        total_tasks = Task.query.count()
        total_profiles = Profile.query.count()
        
        # 今日の日付を取得
        today = datetime.now().date()
        week_ago = today - timedelta(days=7)
        
        # 新規ユーザー（過去7日間）
        new_users = User.query.filter(
            func.date(User.created_at) >= week_ago
        ).count()
        
        # 新規タスク（過去7日間）
        new_tasks = Task.query.filter(
            func.date(Task.created_at) >= week_ago
        ).count()
        
        # 完了したタスク数
        completed_tasks = Task.query.filter_by(status='completed').count()
        
        # 期限切れタスク数
        overdue_tasks = Task.query.filter(
            and_(
                Task.due_date < datetime.now(),
                Task.status != 'completed'
            )
        ).count()
        
        return {
            'total_users': total_users,
            'total_tasks': total_tasks,
            'total_profiles': total_profiles,
            'new_users': new_users,
            'new_tasks': new_tasks,
            'completed_tasks': completed_tasks,
            'overdue_tasks': overdue_tasks
        }
        
    except Exception as e:
        log_error(f"Error getting basic statistics: {e}")
        return {}

def get_task_statistics():
    """タスク関連の統計を取得"""
    try:
        # ステータス別タスク数
        status_counts = db.session.query(
            Task.status, 
            func.count(Task.id).label('count')
        ).group_by(Task.status).all()
        
        status_dict = {status: count for status, count in status_counts}
        
        # 総タスク数
        total_tasks = Task.query.count()
        
        # 完了率を計算
        completed_count = status_dict.get('completed', 0)
        completion_rate = (completed_count / total_tasks * 100) if total_tasks > 0 else 0
        
        # ユーザー別タスク数（上位5人）
        user_task_counts = db.session.query(
            User.name,
            func.count(Task.id).label('task_count')
        ).join(Task).group_by(User.id, User.name).order_by(
            func.count(Task.id).desc()
        ).limit(5).all()
        
        return {
            'status_counts': status_dict,
            'completion_rate': round(completion_rate, 1),
            'user_task_counts': [
                {'name': name, 'count': count} 
                for name, count in user_task_counts
            ]
        }
        
    except Exception as e:
        log_error(f"Error getting task statistics: {e}")
        return {}

def get_chart_data():
    """チャート表示用のデータを取得"""
    try:
        # 過去7日間の日別タスク作成数
        days_data = []
        tasks_data = []
        
        for i in range(6, -1, -1):
            date = datetime.now().date() - timedelta(days=i)
            count = Task.query.filter(
                func.date(Task.created_at) == date
            ).count()
            
            days_data.append(date.strftime('%m/%d'))
            tasks_data.append(count)
        
        # ステータス別パイチャート用データ
        status_counts = db.session.query(
            Task.status,
            func.count(Task.id)
        ).group_by(Task.status).all()
        
        status_labels = []
        status_data = []
        status_colors = {
            'pending': '#ffc107',
            'in_progress': '#17a2b8', 
            'completed': '#28a745'
        }
        colors = []
        
        for status, count in status_counts:
            status_labels.append({
                'pending': '未着手',
                'in_progress': '進行中',
                'completed': '完了'
            }.get(status, status))
            status_data.append(count)
            colors.append(status_colors.get(status, '#6c757d'))
        
        return {
            'line_chart': {
                'labels': days_data,
                'data': tasks_data
            },
            'pie_chart': {
                'labels': status_labels,
                'data': status_data,
                'colors': colors
            }
        }
        
    except Exception as e:
        log_error(f"Error getting chart data: {e}")
        return {}

def get_recent_activities():
    """最近のアクティビティを取得"""
    try:
        # 最近作成されたタスク（上位5件）
        recent_tasks = Task.query.join(User).order_by(
            Task.created_at.desc()
        ).limit(5).all()
        
        # 最近登録されたユーザー（上位3人）
        recent_users = User.query.order_by(
            User.created_at.desc()
        ).limit(3).all()
        
        activities = []
        
        # タスクのアクティビティ
        for task in recent_tasks:
            activities.append({
                'type': 'task',
                'message': f'新しいタスク "{task.title}" が作成されました',
                'user': task.user.name,
                'time': task.created_at.strftime('%m/%d %H:%M'),
                'icon': 'fa-tasks'
            })
        
        # ユーザーのアクティビティ
        for user in recent_users:
            activities.append({
                'type': 'user',
                'message': f'新しいユーザー "{user.name}" が登録されました',
                'user': user.name,
                'time': user.created_at.strftime('%m/%d %H:%M'),
                'icon': 'fa-user-plus'
            })
        
        # 時間順でソート
        activities.sort(key=lambda x: x['time'], reverse=True)
        
        return activities[:8]  # 最新8件を返す
        
    except Exception as e:
        log_error(f"Error getting recent activities: {e}")
        return [] 