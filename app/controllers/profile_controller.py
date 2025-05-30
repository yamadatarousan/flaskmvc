from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models.profile import Profile
from app.models.user import User
from app.forms.profile_form import ProfileForm
from sqlalchemy import or_

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profiles')
@login_required
def profile_list():
    """プロファイル一覧表示"""
    # 検索・フィルタリングパラメータを取得
    search_query = request.args.get('search', '')
    user_filter = request.args.get('user', '')
    sort_by = request.args.get('sort', 'user_name')
    order = request.args.get('order', 'asc')
    
    # ベースクエリ
    query = Profile.query.join(User)
    
    # 検索条件を適用
    if search_query:
        search_pattern = f"%{search_query}%"
        query = query.filter(
            or_(
                User.name.ilike(search_pattern),
                Profile.address.ilike(search_pattern),
                Profile.phone_number.ilike(search_pattern)
            )
        )
    
    # ユーザーフィルター
    if user_filter:
        query = query.filter(Profile.user_id == user_filter)
    
    # ソート条件を適用
    if sort_by == 'user_name':
        if order == 'desc':
            query = query.order_by(User.name.desc())
        else:
            query = query.order_by(User.name.asc())
    elif sort_by == 'address':
        if order == 'desc':
            query = query.order_by(Profile.address.desc())
        else:
            query = query.order_by(Profile.address.asc())
    elif sort_by == 'phone_number':
        if order == 'desc':
            query = query.order_by(Profile.phone_number.desc())
        else:
            query = query.order_by(Profile.phone_number.asc())
    elif sort_by == 'birth_date':
        if order == 'desc':
            query = query.order_by(Profile.birth_date.desc())
        else:
            query = query.order_by(Profile.birth_date.asc())
    else:  # created_at
        if order == 'desc':
            query = query.order_by(Profile.created_at.desc())
        else:
            query = query.order_by(Profile.created_at.asc())
    
    profiles = query.all()
    users_for_filter = User.query.all()
    total_count = Profile.query.count()
    filtered_count = len(profiles)
    
    return render_template('profile_list.html', 
                         profiles=profiles,
                         users_for_filter=users_for_filter,
                         search_query=search_query,
                         user_filter=user_filter,
                         sort_by=sort_by,
                         order=order,
                         total_count=total_count,
                         filtered_count=filtered_count)

@profile_bp.route('/profiles/create', methods=['GET', 'POST'])
@login_required
def create_profile():
    """プロファイル新規作成"""
    form = ProfileForm()
    users = User.query.all()
    
    # SelectFieldの選択肢を設定
    form.user_id.choices = [('', 'ユーザーを選択してください')] + [(user.id, user.name) for user in users]
    
    if form.validate_on_submit():
        try:
            # 既存のプロファイルがないかチェック
            existing_profile = Profile.query.filter_by(user_id=form.user_id.data).first()
            if existing_profile:
                flash('このユーザーのプロファイルは既に存在します。', 'error')
                return render_template('profile_form.html', form=form, users=users, action='新規作成')
            
            profile = Profile(
                birth_date=form.birth_date.data,
                address=form.address.data,
                phone_number=form.phone_number.data,
                user_id=form.user_id.data
            )
            db.session.add(profile)
            db.session.commit()
            flash('プロファイルが正常に作成されました。', 'success')
            return redirect(url_for('profile.profile_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'プロファイルの作成中にエラーが発生しました: {str(e)}', 'error')
    
    return render_template('profile_form.html', form=form, users=users, action='新規作成')

@profile_bp.route('/profiles/<int:profile_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(profile_id):
    """プロファイル編集"""
    profile = Profile.query.get_or_404(profile_id)
    form = ProfileForm(obj=profile)
    users = User.query.all()
    
    # SelectFieldの選択肢を設定
    form.user_id.choices = [('', 'ユーザーを選択してください')] + [(user.id, user.name) for user in users]
    
    if form.validate_on_submit():
        try:
            # 他のユーザーに変更する場合の重複チェック
            if int(form.user_id.data) != profile.user_id:
                existing_profile = Profile.query.filter_by(user_id=form.user_id.data).first()
                if existing_profile:
                    flash('このユーザーのプロファイルは既に存在します。', 'error')
                    return render_template('profile_form.html', form=form, users=users, profile=profile, action='編集')
            
            profile.birth_date = form.birth_date.data
            profile.address = form.address.data
            profile.phone_number = form.phone_number.data
            profile.user_id = form.user_id.data
            db.session.commit()
            flash('プロファイルが正常に更新されました。', 'success')
            return redirect(url_for('profile.profile_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'プロファイルの更新中にエラーが発生しました: {str(e)}', 'error')
    
    return render_template('profile_form.html', form=form, users=users, profile=profile, action='編集')

@profile_bp.route('/profiles/<int:profile_id>/delete', methods=['POST'])
@login_required
def delete_profile(profile_id):
    """プロファイル削除"""
    profile = Profile.query.get_or_404(profile_id)
    
    try:
        db.session.delete(profile)
        db.session.commit()
        flash('プロファイルが正常に削除されました。', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'プロファイルの削除中にエラーが発生しました: {str(e)}', 'error')
    
    return redirect(url_for('profile.profile_list'))

@profile_bp.route('/profiles/<int:profile_id>')
@login_required
def profile_detail(profile_id):
    """プロファイル詳細表示"""
    profile = Profile.query.get_or_404(profile_id)
    return render_template('profile_detail.html', profile=profile) 