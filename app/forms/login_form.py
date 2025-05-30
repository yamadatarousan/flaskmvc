from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError

class LoginForm(FlaskForm):
    email = StringField('メールアドレス', validators=[
        DataRequired(message='メールアドレスは必須です'),
        Email(message='有効なメールアドレスを入力してください')
    ])
    password = PasswordField('パスワード', validators=[
        DataRequired(message='パスワードは必須です'),
        Length(min=6, message='パスワードは6文字以上で入力してください')
    ])
    remember_me = BooleanField('ログイン状態を保持する')
    submit = SubmitField('ログイン')

class RegistrationForm(FlaskForm):
    name = StringField('名前', validators=[
        DataRequired(message='名前は必須です'),
        Length(max=100, message='名前は100文字以内で入力してください')
    ])
    email = StringField('メールアドレス', validators=[
        DataRequired(message='メールアドレスは必須です'),
        Email(message='有効なメールアドレスを入力してください'),
        Length(max=120, message='メールアドレスは120文字以内で入力してください')
    ])
    password = PasswordField('パスワード', validators=[
        DataRequired(message='パスワードは必須です'),
        Length(min=6, message='パスワードは6文字以上で入力してください')
    ])
    password2 = PasswordField('パスワード確認', validators=[
        DataRequired(message='パスワード確認は必須です')
    ])
    submit = SubmitField('登録')

    def validate_password2(self, field):
        if field.data != self.password.data:
            raise ValidationError('パスワードが一致しません')

    def validate_email(self, field):
        from app.models.user import User
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('このメールアドレスは既に登録されています') 