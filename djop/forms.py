from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo, Email
from djop.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(),Length(min=4, max=20)])
    email = StringField('email', validators=[DataRequired(),Email()])
    password = PasswordField('password', validators=[DataRequired(),Length(min=6)])
    confirm_password = PasswordField('confirm password', validators=[DataRequired(),EqualTo('password')])
    address = StringField('addres', validators=[DataRequired()])
    firm_name = StringField('name', validators=[DataRequired()])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('username already taken')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('email already in use')

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(),Length(min=6)])
    rememberMe = BooleanField('remember me')

    submit = SubmitField('Log in')

class UpdatePhoto(FlaskForm):
    photo = FileField('choose file', validators=[FileAllowed(['png','jpg','jpeg']), DataRequired()])

    submit = SubmitField('Update Photo')

class UpdateProfile(FlaskForm):
    username = StringField('username', validators=[DataRequired(),Length(min=4, max=20)])
    email = StringField('email', validators=[DataRequired(),Email()]) 
    address = StringField('addres', validators=[DataRequired()])
    firm_name = StringField('name', validators=[DataRequired()])

    submit = SubmitField('Update Profile')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('username already taken')
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('email already in use')
