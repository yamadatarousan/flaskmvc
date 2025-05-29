from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Optional
from datetime import date

def coerce_int_or_none(value):
    """空文字列をNoneに、それ以外は整数に変換"""
    if value == '' or value is None:
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

class TaskForm(FlaskForm):
    title = StringField('タイトル', validators=[
        DataRequired(message='タイトルは必須です'),
        Length(max=100, message='タイトルは100文字以内で入力してください')
    ])
    description = TextAreaField('説明', validators=[
        Optional(),
        Length(max=500, message='説明は500文字以内で入力してください')
    ])
    status = SelectField('ステータス', choices=[
        ('pending', '待機中'),
        ('in_progress', '進行中'),
        ('completed', '完了')
    ], validators=[DataRequired()])
    due_date = DateField('期限日', validators=[Optional()])
    user_id = SelectField('担当者', validators=[
        DataRequired(message='担当者を選択してください')
    ], coerce=coerce_int_or_none)

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        # デフォルト値を設定
        if not self.status.data:
            self.status.data = 'pending' 