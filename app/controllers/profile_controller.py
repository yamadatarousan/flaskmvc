from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.profile import Profile
from app.models.user import User
from app.forms.profile_form import ProfileForm

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profiles')
def profile_list():
    """プロファイル一覧表示"""
    profiles = Profile.query.join(User).all()
    return render_template('profile_list.html', profiles=profiles)

@profile_bp.route('/profiles/create', methods=['GET', 'POST'])
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
def profile_detail(profile_id):
    """プロファイル詳細表示"""
    profile = Profile.query.get_or_404(profile_id)
    return render_template('profile_detail.html', profile=profile) 