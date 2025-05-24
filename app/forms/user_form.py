from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email, ValidationError
from app.models.user import User

class UserForm(FlaskForm):
    id = HiddenField('ID')
    name = StringField('名前', validators=[DataRequired(message='名前は必須です')])
    email = StringField('メールアドレス', validators=[
        DataRequired(message='メールアドレスは必須です'),
        Email(message='有効なメールアドレスを入力してください')
    ])
    submit = SubmitField('保存')

    def validate_email(self, field):
        """メールアドレスの重複チェック"""
        # 新規作成時または編集時で自分以外のメールアドレスとの重複をチェック
        user_id = self.id.data
        
        # フォームにIDがある場合（編集時）
        if user_id:
            user = User.query.filter(User.email == field.data, User.id != int(user_id)).first()
        else:
            user = User.query.filter_by(email=field.data).first()
            
        if user:
            raise ValidationError('このメールアドレスは既に使用されています') 