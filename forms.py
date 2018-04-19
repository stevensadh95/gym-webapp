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
    state = SelectField("State",choices=[('AL','AL'),('AK','AK'),('AZ','AZ'),('AR','AR'),('CA','CA'),('CO','CO'),('CT','CT'),('DE','DE'),('FL','FL'),('GA','GA'),('HI','HI'),('ID','ID'),('IL','IL'),('IN','IN'),('IA','IA'),('KS','KS'),('KY','KY'),('LA','LA'),('ME','ME'),('MD','MD'),('MA','MA'),('MI','MI'),('MN','MN'),('MS','MS'),('MO','MO'),('MT','MT'),('NE','NE'),('NV','NV'),('NH','NH'),('NJ','NJ'),('NM','NM'),('NY','NY'),('NC','NC'),('ND','ND'),('OH','OH'),('OK','OK'),('OR','OR'),('PA','PA'),('RI','RI'),('SC','SC'),('SD','SD'),('TN','TN'),('TX','TX'),('UT','UT'),('VT','VT'),('VA','VA'),('WA','WA'),('WV','WV'),('WI','WI'),('WY','WY)],validators=[DataRequired()])
    sex = RadioField("Sex",choices=[('Male','Male'),('Female','Female')],validators=[DataRequired()])
    birthday = DateField("DatePicker", validators=[DataRequired()])
    picture = FileField("Image",validators=[DataRequired(),FileAllowed(['jpg', 'png'], 'Images only!')])
    bio = StringField("Bio")

    # def validate_username(self,username):
    #     user = User.query.filter_by(username=username.data).first()
    #
    #     if not User:
    #         raise ValidationError("username already exists")


