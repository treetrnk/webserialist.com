from flask_wtf import FlaskForm
from wtforms import (
        StringField, TextAreaField, SelectField, IntegerField, SubmitField, 
        BooleanField, SubmitField, DateTimeField, SelectMultipleField, 
        PasswordField, HiddenField, DateField, TimeField, FileField
)
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, Email, Optional, EqualTo, ValidationError
from app.models import User

required = "<span class='text-danger'>*</span>"

class SignupForm(FlaskForm):
    username = StringField(f'Username{required}', validators=[DataRequired(), Length(max=64)])
    email = StringField(f'Email{required}', validators=[Length(max=120)])
    first_name = StringField('First Name', validators=[Length(max=100)])
    last_name = StringField('Last Name', validators=[Length(max=100)])
    password = PasswordField(f'Password{required}', validators=[DataRequired(), Length(max=128)])
    confirm_password = PasswordField(f'Confirm Password{required}', validators=[DataRequired(), EqualTo('password'), Length(max=128)])

    def validate_username(self, username):
        user = User.query.filter_by(username=self.username.data).first()
        if user is not None:
            raise ValidationError('Username already in use.', 'danger')
        return True

    def validate_email(self, email):
        user = User.query.filter_by(email=self.email.data).first()
        if user is not None:
            raise ValidationError('Email address already in use.', 'danger')
        return True

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ProfileEditForm(FlaskForm):
    username = StringField(f'Username{required}', validators=[DataRequired(), Length(max=64)])
    email = StringField(f'Email{required}', validators=[Length(max=120), Email()])
    first_name = StringField('First Name', validators=[Length(max=100)])
    last_name = StringField('Last Name', validators=[Length(max=100)])
    avatar = FileField('Avatar', validators=[Length(max=500)])
    website = StringField('Website', validators=[Length(max=300)])
    about_me = TextAreaField('About Me', validators=[Length(max=140)])
    theme = SelectField('Theme', validators=[Length(max=75)])
    timezone = SelectField('Timezone', validators=[Length(max=150)])
