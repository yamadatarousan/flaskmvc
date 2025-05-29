from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Optional, Regexp
from datetime import date

def coerce_int_or_none(value):
    """空文字列をNoneに、それ以外は整数に変換"""
    if value == '' or value is None:
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

class ProfileForm(FlaskForm):
    birth_date = DateField('生年月日', validators=[Optional()])
    address = StringField('住所', validators=[
        Optional(),
        Length(max=200, message='住所は200文字以内で入力してください')
    ])
    phone_number = StringField('電話番号', validators=[
        Optional(),
        Length(max=20, message='電話番号は20文字以内で入力してください'),
        Regexp(r'^[0-9\-\+\(\)]*$', message='電話番号は数字、ハイフン、プラス、括弧のみ使用可能です')
    ])
    user_id = SelectField('ユーザー', validators=[
        DataRequired(message='ユーザーを選択してください')
    ], coerce=coerce_int_or_none) 