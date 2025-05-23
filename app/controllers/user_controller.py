# app/controllers/user_controller.py
from flask import Blueprint, render_template, current_app
from app.models.user import User
import logging

# ログ設定
logger = logging.getLogger(__name__)

bp = Blueprint('user', __name__, url_prefix='/users')

@bp.route('/')
@bp.route('')
def list_users():
    try:
        logger.info("Accessing user list route")
        users = User.query.all()
        logger.info(f"Found {len(users)} users")
        return render_template('user_list.html', users=users)
    except Exception as e:
        logger.error(f"Error in list_users: {e}")
        return render_template('error.html', error=str(e)), 500

# ルートURL用に新しいブループリントを作成
root_bp = Blueprint('root', __name__)

@root_bp.route('/')
def index():
    try:
        logger.info("Accessing root index route")
        users = User.query.all()
        logger.info(f"Found {len(users)} users for root index")
        return render_template('user_list.html', users=users)
    except Exception as e:
        logger.error(f"Error in index: {e}")
        return render_template('error.html', error=str(e)), 500