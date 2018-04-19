from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SubmitField,SelectField
from wtforms.validators import DataRequired,ValidationError
from wtforms.fields.html5 import DateField
from flask_wtf.file import FileField,FileAllowed

class LoginForm(FlaskForm):
    username= StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField('Log in')

class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField('Sign up')

class ProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email",validators=[DataRequired()])
    state = SelectField("State",choices=[('NH','Fl')],validators=[DataRequired()])
    sex = RadioField("Sex",choices=[('Male','Male'),('Female','Female')],validators=[DataRequired()])
    birthday = DateField("DatePicker", validators=[DataRequired()])
    picture = FileField("Image",validators=[DataRequired(),FileAllowed(['jpg', 'png'], 'Images only!')])
    bio = StringField("Bio")

    # def validate_username(self,username):
    #     user = User.query.filter_by(username=username.data).first()
    #
    #     if not User:
    #         raise ValidationError("username already exists")


