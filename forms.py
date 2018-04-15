from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired,ValidationError

class LoginForm(FlaskForm):
    username= StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField('Log in')

class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField('Sign up')

    # def validate_username(self,username):
    #     user = User.query.filter_by(username=username.data).first()
    #
    #     if not User:
    #         raise ValidationError("username already exists")


